class ProfileService:

    @staticmethod
    def update_profile(profile, data):
        for key, value in data.items():
            setattr(profile, key, value)
        profile.save()
        return profile