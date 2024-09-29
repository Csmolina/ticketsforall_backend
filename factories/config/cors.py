def cors_config():
    return {
        "allow_origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "OPTIONS", "PUT"],
        "allow_headers": ["*"],
    }
