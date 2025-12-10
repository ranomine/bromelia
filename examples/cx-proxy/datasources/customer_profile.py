from typing import Optional, List
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class CustomerProfile:
    """
    Represents a customer profile configuration.
    """
    profileName: str
    hssRealm: str
    imsRealm: str
    allowEmptyResultForGtpHubInfo: bool = False
    apnRulesetName: str = "default"
    breakoutZoneName: str = "default"
    customer: Optional[str] = None
    detectHlrWrongMsisdn: bool = True
    forceSponsorId: Optional[str] = None
    ggsnConfigs: Optional[str] = None
    hlrNumber: Optional[str] = None
    hssHost: str = ""
    mgtDigitsToReplace: int = 6
    mgtPrefix: str = ""
    pgwRulesetName: str = "default"
    preventCamelContinue: bool = False
    preventMsisdnTranslation: bool = False
    scfNumber: Optional[str] = None
    skipRhPrefix: bool = False
    skipRhSuffix: bool = False
    smscNumber: Optional[str] = None
    unmapForGtpHubInfo: bool = False
    unodeRulesetName: str = "default"
    useMgtRouting: bool = False
    userSupplied: Optional[str] = None
    ussdDcsRewrite: Optional[str] = None

    def __post_init__(self):
        """Validate profile"""
        if not self.profileName:
            raise ValueError("Profile name cannot be empty")


class CustomerProfileManager:
    """
    Manages a collection of customer profiles for the Diameter proxy.
    """

    def __init__(self):
        self._profiles: List[CustomerProfile] = []
        self._index: dict[str, CustomerProfile] = {}

    def add_profile(self, profile: CustomerProfile) -> None:
        """
        Add a new customer profile to the collection.

        Args:
            profile: CustomerProfile instance to add

        Raises:
            ValueError: If profileName already exists
        """
        if profile.profileName in self._index:
            raise ValueError(
                f"Profile {profile.profileName} already exists"
            )

        self._profiles.append(profile)
        self._index[profile.profileName] = profile

    def get_profile_by_name(self, profile_name: str) -> Optional[CustomerProfile]:
        """
        Retrieve a customer profile by name.

        Args:
            profile_name: The profile name to look up

        Returns:
            CustomerProfile instance if found, None otherwise
        """
        return self._index.get(profile_name)

    def remove_profile(self, profile_name: str) -> bool:
        """
        Remove a profile by name.

        Args:
            profile_name: The profile name to remove

        Returns:
            True if profile was removed, False if not found
        """
        if profile_name not in self._index:
            return False

        profile = self._index.pop(profile_name)
        self._profiles.remove(profile)
        return True

    def get_all_profiles(self) -> List[CustomerProfile]:
        """Return all profiles."""
        return self._profiles.copy()

    def __len__(self) -> int:
        """Return number of profiles."""
        return len(self._profiles)

    def save_to_json(self, filepath: str) -> None:
        """
        Save all profiles to a JSON file.

        Args:
            filepath: Path to the JSON file

        Raises:
            IOError: If file cannot be written
        """
        data = {
            "profiles": [asdict(profile) for profile in self._profiles]
        }

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_json(self, filepath: str, clear_existing: bool = True) -> int:
        """
        Load profiles from a JSON file.

        Args:
            filepath: Path to the JSON file
            clear_existing: If True, clear existing profiles before loading

        Returns:
            Number of profiles loaded

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON format is invalid or contains duplicate names
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict) or 'profiles' not in data:
            raise ValueError("Invalid JSON format: expected {'profiles': [...]}")

        if clear_existing:
            self._profiles.clear()
            self._index.clear()

        loaded_count = 0
        for profile_data in data['profiles']:
            profile = CustomerProfile(**profile_data)
            self.add_profile(profile)
            loaded_count += 1

        return loaded_count


# Example usage
if __name__ == "__main__":
    # Initialize the manager
    manager = CustomerProfileManager()

    # Load from JSON file
    json_file = "../config/customer_profiles.json"
    try:
        count = manager.load_from_json(json_file)
        print(f"Loaded {count} profiles from {json_file}")

        # Retrieve by name
        result = manager.get_profile_by_name("KnowRoamingHSS")
        if result:
            print(f"\nFound profile: {result.profileName}")
            print(f"  HSS Realm: {result.hssRealm}")
            print(f"  IMS Realm: {result.imsRealm}")
            print(f"  SMSC Number: {result.smscNumber}")
    except FileNotFoundError:
        print(f"File not found: {json_file}")
