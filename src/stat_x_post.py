import requests

def x_post(secrets, message):
    cookies = secrets['cookies']
    headers = secrets['headers']
    queryId = secrets['queryId']

    if (len(message) == 0):
        print("")
        return 0

    json_data = {
        'variables': {
            'tweet_text': message,
            'dark_request': False,
            'media': {
                'media_entities': [],
                'possibly_sensitive': False,
            },
            'semantic_annotation_ids': [],
            'disallowed_reply_options': None,
        },
        'features': {
            'premium_content_api_read_enabled': False,
            'communities_web_enable_tweet_community_results_fetch': True,
            'c9s_tweet_anatomy_moderator_badge_enabled': True,
            'responsive_web_grok_analyze_button_fetch_trends_enabled': False,
            'responsive_web_grok_analyze_post_followups_enabled': True,
            'responsive_web_jetfuel_frame': False,
            'responsive_web_grok_share_attachment_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'responsive_web_twitter_article_tweet_consumption_enabled': True,
            'tweet_awards_web_tipping_enabled': False,
            'responsive_web_grok_show_grok_translated_post': False,
            'responsive_web_grok_analysis_button_from_backend': True,
            'creator_subscriptions_quote_tweet_preview_enabled': False,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'profile_label_improvements_pcf_label_in_post_enabled': True,
            'rweb_tipjar_consumption_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': False,
            'articles_preview_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'responsive_web_grok_image_annotation_enabled': True,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_enhance_cards_enabled': False,
        },
        'queryId': queryId,
    }

    response = requests.post(
        f'https://x.com/i/api/graphql/{queryId}/CreateTweet',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    
    return response.status_code