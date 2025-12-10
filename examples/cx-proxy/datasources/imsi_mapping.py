from typing import Optional, List
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class ImsiMapping:
    """
    Represents a mapping between sponsored and customer identities.
    """
    sponsoredImsi: str
    sponsoredMsisdn: str
    customerImsi: str
    customerMsisdn: str
    customerProfileName: str
    sponsorName: str
    sponsorId: str = ""
    userSupplied: Optional[str] = None
    imsiBarred: bool = False

    def __post_init__(self):
        """Validate IMSI format (basic validation)"""
        if not self.sponsoredImsi or not self.customerImsi:
            raise ValueError("IMSI fields cannot be empty")


class ImsiMappingManager:
    """
    Manages a collection of IMSI mappings for the Diameter proxy.
    """
    
    def __init__(self):
        self._mappings: List[ImsiMapping] = []
        self._index: dict[str, ImsiMapping] = {}
    
    def add_mapping(self, mapping: ImsiMapping) -> None:
        """
        Add a new IMSI mapping to the collection.
        
        Args:
            mapping: ImsiMapping instance to add
            
        Raises:
            ValueError: If sponsoredImsi already exists
        """
        if mapping.sponsoredImsi in self._index:
            raise ValueError(
                f"Mapping for sponsored IMSI {mapping.sponsoredImsi} already exists"
            )
        
        self._mappings.append(mapping)
        self._index[mapping.sponsoredImsi] = mapping
    
    def get_mapping_by_sponsored_imsi(self, sponsored_imsi: str) -> Optional[ImsiMapping]:
        """
        Retrieve an IMSI mapping by sponsored IMSI.
        
        Args:
            sponsored_imsi: The sponsored IMSI to look up
            
        Returns:
            ImsiMapping instance if found, None otherwise
        """
        return self._index.get(sponsored_imsi)
    
    def remove_mapping(self, sponsored_imsi: str) -> bool:
        """
        Remove a mapping by sponsored IMSI.
        
        Args:
            sponsored_imsi: The sponsored IMSI to remove
            
        Returns:
            True if mapping was removed, False if not found
        """
        if sponsored_imsi not in self._index:
            return False
        
        mapping = self._index.pop(sponsored_imsi)
        self._mappings.remove(mapping)
        return True
    
    def get_all_mappings(self) -> List[ImsiMapping]:
        """Return all mappings."""
        return self._mappings.copy()
    
    def get_mappings_by_sponsor(self, sponsor_name: str) -> List[ImsiMapping]:
        """
        Get all mappings for a specific sponsor.
        
        Args:
            sponsor_name: Name of the sponsor
            
        Returns:
            List of ImsiMapping instances for the sponsor
        """
        return [m for m in self._mappings if m.sponsorName == sponsor_name]
    
    def get_mapping_by_customer_imsi(self, customer_imsi: str) -> Optional[ImsiMapping]:
        """
        Find mapping by customer IMSI (slower lookup).

        Args:
            customer_imsi: The customer IMSI to look up

        Returns:
            ImsiMapping instance if found, None otherwise
        """
        for mapping in self._mappings:
            if mapping.customerImsi == customer_imsi:
                return mapping
        return None

    def get_mapping_by_customer_msisdn(self, customer_msisdn: str) -> Optional[ImsiMapping]:
        """
        Find mapping by customer MSISDN (slower lookup).

        Args:
            customer_msisdn: The customer MSISDN to look up

        Returns:
            ImsiMapping instance if found, None otherwise
        """
        for mapping in self._mappings:
            if mapping.customerMsisdn == customer_msisdn:
                return mapping
        return None
    
    def load_from_list(self, mappings: List[dict]) -> None:
        """
        Load multiple mappings from a list of dictionaries.
        
        Args:
            mappings: List of dicts with mapping data
        """
        for data in mappings:
            mapping = ImsiMapping(**data)
            self.add_mapping(mapping)
    
    def __len__(self) -> int:
        """Return number of mappings."""
        return len(self._mappings)
    
    def save_to_json(self, filepath: str) -> None:
        """
        Save all mappings to a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Raises:
            IOError: If file cannot be written
        """
        data = {
            "mappings": [asdict(mapping) for mapping in self._mappings]
        }
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_json(self, filepath: str, clear_existing: bool = True) -> int:
        """
        Load mappings from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            clear_existing: If True, clear existing mappings before loading
            
        Returns:
            Number of mappings loaded
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON format is invalid or contains duplicate sponsored IMSIs
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict) or 'mappings' not in data:
            raise ValueError("Invalid JSON format: expected {'mappings': [...]}")
        
        if clear_existing:
            self._mappings.clear()
            self._index.clear()
        
        loaded_count = 0
        for mapping_data in data['mappings']:
            mapping = ImsiMapping(**mapping_data)
            self.add_mapping(mapping)
            loaded_count += 1
        
        return loaded_count


# Example usage
if __name__ == "__main__":
    # Initialize the manager
    manager = ImsiMappingManager()
    
    # Create sample mappings
    mapping1 = ImsiMapping(
        sponsoredImsi="310150123456789",
        sponsoredMsisdn="+1234567890",
        customerImsi="310150987654321",
        customerMsisdn="+0987654321",
        customerProfileName="Premium User",
        sponsorName="Corporate Sponsor A",
        sponsorId="SPONSOR_001",
        userSupplied="admin@example.com",
        imsiBarred=False
    )
    
    mapping2 = ImsiMapping(
        sponsoredImsi="310150111222333",
        sponsoredMsisdn="+1111222333",
        customerImsi="310150444555666",
        customerMsisdn="+4445556666",
        customerProfileName="Basic User",
        sponsorName="Corporate Sponsor B",
        sponsorId="SPONSOR_002",
        userSupplied=None,
        imsiBarred=True
    )
    
    # Add mappings
    manager.add_mapping(mapping1)
    manager.add_mapping(mapping2)
    
    # Retrieve by sponsored IMSI
    result = manager.get_mapping_by_sponsored_imsi("310150123456789")
    if result:
        print(f"Found mapping:")
        print(f"  Customer IMSI: {result.customerImsi}")
        print(f"  Customer MSISDN: {result.customerMsisdn}")
        print(f"  Profile: {result.customerProfileName}")
        print(f"  Sponsor: {result.sponsorName}")
    
    # Get all mappings for a sponsor
    sponsor_mappings = manager.get_mappings_by_sponsor("Corporate Sponsor A")
    print(f"\nMappings for Corporate Sponsor A: {len(sponsor_mappings)}")
    
    # Save to JSON file
    json_file = "imsi_mappings.json"
    manager.save_to_json(json_file)
    print(f"\nSaved {len(manager)} mappings to {json_file}")
    
    # Load from JSON file
    new_manager = ImsiMappingManager()
    count = new_manager.load_from_json(json_file)
    print(f"Loaded {count} mappings from {json_file}")
    
    # Verify loaded data
    loaded_mapping = new_manager.get_mapping_by_sponsored_imsi("310150123456789")
    if loaded_mapping:
        print(f"\nVerified loaded mapping for sponsored IMSI 310150123456789:")
        print(f"  Customer Profile: {loaded_mapping.customerProfileName}")
