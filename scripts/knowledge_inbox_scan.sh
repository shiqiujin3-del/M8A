#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/Users/shiqiujing/Documents/M8A"
PRODUCT_ID="product_hk620"
PRODUCT_MODEL="HK620"
INBOX_DIR="$PROJECT_ROOT/knowledge/products/HK620/inbox"
TMP_SQL="/private/tmp/m8a_hk620_inbox_scan.sql"
UPLOADER="${USER:-unknown}"

sql_escape() {
  printf "%s" "$1" | sed "s/'/''/g"
}

detect_type() {
  case "$1" in
    pdf) echo "PDF" ;;
    doc|docx) echo "Word" ;;
    xls|xlsx|csv) echo "Excel" ;;
    jpg|jpeg|png|webp|gif|tif|tiff) echo "Image" ;;
    mp4|mov|avi|mkv|webm) echo "Video" ;;
    md|markdown) echo "Markdown" ;;
    txt) echo "TXT" ;;
    *) echo "Unsupported" ;;
  esac
}

cat > "$TMP_SQL" <<'SQL'
create table if not exists m8a_knowledge_inbox_files (
  inbox_file_id text primary key,
  product_id text not null,
  product_model text not null,
  file_name text not null,
  file_path text not null unique,
  file_extension text not null,
  file_type text not null,
  file_size_bytes bigint not null,
  file_hash text not null,
  source_directory text not null,
  uploaded_at timestamptz not null,
  uploaded_by text not null,
  is_duplicate boolean not null default false,
  duplicate_of text,
  registration_status text not null default 'registered',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists m8a_knowledge_processing_queue (
  queue_id text primary key,
  inbox_file_id text not null references m8a_knowledge_inbox_files(inbox_file_id),
  product_id text not null,
  product_model text not null,
  status text not null,
  current_step text not null,
  allowed_next_statuses text[] not null,
  can_update_golden_knowledge boolean not null default false,
  can_update_postgres boolean not null default false,
  can_update_qdrant boolean not null default false,
  can_update_chunks boolean not null default false,
  reviewer text,
  review_notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
SQL

while IFS= read -r -d '' file; do
  name="$(basename "$file")"
  if [[ "$name" == "INDEX.md" ]]; then
    continue
  fi

  ext="${name##*.}"
  ext="$(printf "%s" "$ext" | tr '[:upper:]' '[:lower:]')"
  type="$(detect_type "$ext")"
  if [[ "$type" == "Unsupported" ]]; then
    continue
  fi

  size="$(stat -f%z "$file")"
  hash="$(shasum -a 256 "$file" | awk '{print $1}')"
  uploaded_at="$(stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "$file")"
  inbox_file_id="inbox_${PRODUCT_MODEL}_${hash:0:16}"
  queue_id="queue_${PRODUCT_MODEL}_${hash:0:16}"

  esc_name="$(sql_escape "$name")"
  esc_file="$(sql_escape "$file")"
  esc_dir="$(sql_escape "$INBOX_DIR")"
  esc_uploader="$(sql_escape "$UPLOADER")"

  cat >> "$TMP_SQL" <<SQL
with existing_hash as (
  select inbox_file_id
  from m8a_knowledge_inbox_files
  where file_hash = '$hash'
    and file_path <> '$esc_file'
  order by created_at asc
  limit 1
),
upsert_file as (
  insert into m8a_knowledge_inbox_files (
    inbox_file_id,
    product_id,
    product_model,
    file_name,
    file_path,
    file_extension,
    file_type,
    file_size_bytes,
    file_hash,
    source_directory,
    uploaded_at,
    uploaded_by,
    is_duplicate,
    duplicate_of,
    registration_status,
    updated_at
  )
  values (
    '$inbox_file_id',
    '$PRODUCT_ID',
    '$PRODUCT_MODEL',
    '$esc_name',
    '$esc_file',
    '$ext',
    '$type',
    $size,
    '$hash',
    '$esc_dir',
    '$uploaded_at',
    '$esc_uploader',
    exists(select 1 from existing_hash),
    (select inbox_file_id from existing_hash),
    'registered',
    now()
  )
  on conflict (file_path) do update set
    file_size_bytes = excluded.file_size_bytes,
    file_hash = excluded.file_hash,
    file_type = excluded.file_type,
    uploaded_at = excluded.uploaded_at,
    uploaded_by = excluded.uploaded_by,
    is_duplicate = excluded.is_duplicate,
    duplicate_of = excluded.duplicate_of,
    updated_at = now()
  returning inbox_file_id, product_id, product_model
)
insert into m8a_knowledge_processing_queue (
  queue_id,
  inbox_file_id,
  product_id,
  product_model,
  status,
  current_step,
  allowed_next_statuses,
  can_update_golden_knowledge,
  can_update_postgres,
  can_update_qdrant,
  can_update_chunks,
  updated_at
)
select
  '$queue_id',
  inbox_file_id,
  product_id,
  product_model,
  'new',
  'file_registered',
  array['processing', 'archived'],
  false,
  false,
  false,
  false,
  now()
from upsert_file
on conflict (queue_id) do update set
  updated_at = now();
SQL
done < <(find "$INBOX_DIR" -type f -print0)

docker exec -i m8a-postgres psql -U m8a -d m8a < "$TMP_SQL"

docker exec m8a-postgres psql -U m8a -d m8a -c "
select
  count(*) as registered_files,
  count(*) filter (where is_duplicate) as duplicate_files
from m8a_knowledge_inbox_files
where product_id = '$PRODUCT_ID';
"

docker exec m8a-postgres psql -U m8a -d m8a -c "
select status, count(*) as queue_count
from m8a_knowledge_processing_queue
where product_id = '$PRODUCT_ID'
group by status
order by status;
"
