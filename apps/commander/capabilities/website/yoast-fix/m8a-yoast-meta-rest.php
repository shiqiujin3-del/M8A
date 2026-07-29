<?php
/**
 * Plugin Name: M8A Yoast SEO Meta REST Fix
 * Description: Exposes _yoast_wpseo_title and _yoast_wpseo_metadesc via WordPress REST API so M8A Commander can set Yoast SEO meta through the standard post endpoint.
 * Version: 1.0.0
 * Author: M8A Infrastructure
 * License: Internal Use Only
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Register Yoast SEO meta keys for REST API access.
 * Without this, WordPress ignores _yoast_wpseo_* in REST API meta payloads
 * because they start with underscore (treated as protected meta).
 */
function m8a_register_yoast_meta_for_rest(): void {
    $meta_keys = [
        '_yoast_wpseo_title',
        '_yoast_wpseo_metadesc',
        '_yoast_wpseo_focuskw',
        '_yoast_wpseo_meta-robots-noindex',
        '_yoast_wpseo_meta-robots-nofollow',
        '_yoast_wpseo_canonical',
    ];

    foreach ($meta_keys as $key) {
        register_post_meta('post', $key, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => 'string',
            'auth_callback' => function () {
                return current_user_can('edit_posts');
            },
            'sanitize_callback' => 'sanitize_text_field',
        ]);
    }
}
add_action('init', 'm8a_register_yoast_meta_for_rest');

/**
 * Custom REST endpoint for bulk-setting Yoast SEO meta on a post.
 * POST /wp-json/m8a/v1/yoast-meta
 * Body: { "post_id": 481, "meta_title": "...", "meta_description": "..." }
 */
function m8a_register_yoast_meta_endpoint(): void {
    register_rest_route('m8a/v1', '/yoast-meta', [
        'methods'             => 'POST',
        'callback'            => 'm8a_set_yoast_meta_callback',
        'permission_callback' => function () {
            return current_user_can('edit_posts');
        },
        'args' => [
            'post_id'          => ['required' => true, 'type' => 'integer'],
            'meta_title'       => ['required' => false, 'type' => 'string'],
            'meta_description' => ['required' => false, 'type' => 'string'],
            'focus_keyword'    => ['required' => false, 'type' => 'string'],
        ],
    ]);
}
add_action('rest_api_init', 'm8a_register_yoast_meta_endpoint');

function m8a_set_yoast_meta_callback(WP_REST_Request $request): WP_REST_Response {
    $post_id = $request->get_param('post_id');
    $post = get_post($post_id);

    if (!$post) {
        return new WP_REST_Response(['success' => false, 'error' => 'Post not found'], 404);
    }

    $updates = [];

    $meta_title = $request->get_param('meta_title');
    if ($meta_title !== null) {
        update_post_meta($post_id, '_yoast_wpseo_title', sanitize_text_field($meta_title));
        $updates['_yoast_wpseo_title'] = $meta_title;
    }

    $meta_description = $request->get_param('meta_description');
    if ($meta_description !== null) {
        update_post_meta($post_id, '_yoast_wpseo_metadesc', sanitize_text_field($meta_description));
        $updates['_yoast_wpseo_metadesc'] = $meta_description;
    }

    $focus_keyword = $request->get_param('focus_keyword');
    if ($focus_keyword !== null) {
        update_post_meta($post_id, '_yoast_wpseo_focuskw', sanitize_text_field($focus_keyword));
        $updates['_yoast_wpseo_focuskw'] = $focus_keyword;
    }

    return new WP_REST_Response([
        'success'  => true,
        'post_id'  => $post_id,
        'updates'  => $updates,
        'verified' => [
            '_yoast_wpseo_title'   => get_post_meta($post_id, '_yoast_wpseo_title', true),
            '_yoast_wpseo_metadesc' => get_post_meta($post_id, '_yoast_wpseo_metadesc', true),
        ],
    ], 200);
}
