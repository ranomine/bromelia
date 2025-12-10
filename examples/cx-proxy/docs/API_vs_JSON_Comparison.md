# REST API vs JSON Files - Field Comparison

This document compares the fields available in the REST API responses versus the local JSON configuration files.

## API Endpoints Discovered

Based on analysis of `ImsiMapping_API.pcapng`:

1. **IMSI Mapping Query**
   - Endpoint: `GET /v1/queryMapping/{sponsoredImsi}`
   - Base URL: `http://localhost:1705` (example from pcapng)
   - Returns: JSON object with IMSI mapping and embedded customer profile info

2. **Emergency Alias** (discovered but not analyzed)
   - Endpoint: `GET /v1/emergencyAlias/{param}`

**Note:** There is **NO separate customer profile API endpoint** in the captured traffic. Customer profile information is embedded within the IMSI mapping response.

---

## IMSI Mapping Comparison

### Fields in Local JSON (`config/imsi_mappings.json`)

```json
{
  "sponsoredImsi": "732123201256920",
  "sponsoredMsisdn": "573150001156920",
  "customerImsi": "312300003093927",
  "customerMsisdn": "879000003093927",
  "customerProfileName": "KnowRoamingHSS",
  "sponsorName": "IMSI21",
  "sponsorId": "21",
  "userSupplied": null,
  "imsiBarred": false
}
```

### Fields in REST API Response

```json
{
  "sponsorId": "22",
  "customerImsi": "901800020930357",
  "customerMsisdn": null,
  "replaceStart": 1,
  "replaceWith": "9018000209",
  "hssRealm": "epc.mnc080.mcc901.3gppnetwork.org",
  "replaceEnd": 11,
  "sponsoredMsisdn": "447382011130357",
  "sponsoredMsisdnLength": 15,
  "customerProfileName": "floliveEU",
  "hssHost": "",
  "sponsoredImsi": "234106479730357",
  "customerIsmi": "901800020930357",
  "userSupplied": null,
  "imsiBarred": false,
  "sponsoredImsiPrefix": "2341064797",
  "sponsorName": "IMSI22",
  "type": "dynamic",
  "sponsoredMsisdnBase": "4473820111"
}
```

### IMSI Mapping: Field-by-Field Analysis

| Field | JSON File | REST API | Notes |
|-------|-----------|----------|-------|
| `sponsoredImsi` | ✅ | ✅ | Present in both |
| `sponsoredMsisdn` | ✅ | ✅ | Present in both |
| `customerImsi` | ✅ | ✅ | Present in both |
| `customerMsisdn` | ✅ | ✅ | Present in both (sometimes null in API) |
| `customerProfileName` | ✅ | ✅ | Present in both |
| `sponsorName` | ✅ | ✅ | Present in both |
| `sponsorId` | ✅ | ✅ | Present in both |
| `userSupplied` | ✅ | ✅ | Present in both |
| `imsiBarred` | ✅ | ✅ | Present in both |
| `replaceStart` | ❌ | ✅ | **API only** - IMSI replacement logic |
| `replaceWith` | ❌ | ✅ | **API only** - Replacement string |
| `replaceEnd` | ❌ | ✅ | **API only** - End position for replacement |
| `hssRealm` | ❌ | ✅ | **API only** - HSS realm (customer profile data) |
| `hssHost` | ❌ | ✅ | **API only** - HSS host (customer profile data) |
| `sponsoredMsisdnLength` | ❌ | ✅ | **API only** - Length of sponsored MSISDN |
| `customerIsmi` | ❌ | ✅ | **API only** - Duplicate/typo of customerImsi |
| `sponsoredImsiPrefix` | ❌ | ✅ | **API only** - Prefix extraction |
| `type` | ❌ | ✅ | **API only** - Mapping type (e.g., "dynamic") |
| `sponsoredMsisdnBase` | ❌ | ✅ | **API only** - Base MSISDN |

### Summary: IMSI Mapping

**Fields MISSING from API (present in JSON):** None - all JSON fields are available in API

**Extra fields in API (not in JSON):**
- `replaceStart`, `replaceWith`, `replaceEnd` - IMSI replacement logic
- `hssRealm`, `hssHost` - Customer profile information
- `sponsoredMsisdnLength`, `sponsoredImsiPrefix`, `sponsoredMsisdnBase` - Derived/computed values
- `type` - Mapping type indicator
- `customerIsmi` - Apparent typo/duplicate field

---

## Customer Profile Comparison

### Fields in Local JSON (`config/customer_profiles.json`)

```json
{
  "allowEmptyResultForGtpHubInfo": false,
  "apnRulesetName": "default",
  "breakoutZoneName": "default",
  "customer": null,
  "detectHlrWrongMsisdn": true,
  "forceSponsorId": null,
  "ggsnConfigs": null,
  "hlrNumber": null,
  "hssHost": "",
  "hssRealm": "hss-summa-1.epc.mnc840.mcc310.3gppnetwork.org",
  "imsRealm": "ims.mnc300.mcc312.3gppnetwork.org",
  "mgtDigitsToReplace": 6,
  "mgtPrefix": "805010",
  "pgwRulesetName": "default",
  "preventCamelContinue": false,
  "preventMsisdnTranslation": false,
  "profileName": "KnowRoamingHSS",
  "scfNumber": null,
  "skipRhPrefix": false,
  "skipRhSuffix": false,
  "smscNumber": "14174000086",
  "unmapForGtpHubInfo": false,
  "unodeRulesetName": "default",
  "useMgtRouting": true,
  "userSupplied": null,
  "ussdDcsRewrite": null
}
```

### Fields Available in REST API

**Important:** The REST API does **NOT** have a separate customer profile endpoint. Only limited customer profile information is embedded in the IMSI mapping response:

```json
{
  "hssRealm": "epc.mnc080.mcc901.3gppnetwork.org",
  "hssHost": "",
  "customerProfileName": "floliveEU"
}
```

### Customer Profile: Field-by-Field Analysis

| Field | JSON File | REST API | Notes |
|-------|-----------|----------|-------|
| `profileName` | ✅ | ✅ (as `customerProfileName`) | Present in both |
| `hssRealm` | ✅ | ✅ | Present in both |
| `hssHost` | ✅ | ✅ | Present in both |
| `imsRealm` | ✅ | ❌ | **MISSING from API** |
| `smscNumber` | ✅ | ❌ | **MISSING from API** |
| `mgtDigitsToReplace` | ✅ | ❌ | **MISSING from API** |
| `mgtPrefix` | ✅ | ❌ | **MISSING from API** |
| `useMgtRouting` | ✅ | ❌ | **MISSING from API** |
| `allowEmptyResultForGtpHubInfo` | ✅ | ❌ | **MISSING from API** |
| `apnRulesetName` | ✅ | ❌ | **MISSING from API** |
| `breakoutZoneName` | ✅ | ❌ | **MISSING from API** |
| `customer` | ✅ | ❌ | **MISSING from API** |
| `detectHlrWrongMsisdn` | ✅ | ❌ | **MISSING from API** |
| `forceSponsorId` | ✅ | ❌ | **MISSING from API** |
| `ggsnConfigs` | ✅ | ❌ | **MISSING from API** |
| `hlrNumber` | ✅ | ❌ | **MISSING from API** |
| `pgwRulesetName` | ✅ | ❌ | **MISSING from API** |
| `preventCamelContinue` | ✅ | ❌ | **MISSING from API** |
| `preventMsisdnTranslation` | ✅ | ❌ | **MISSING from API** |
| `scfNumber` | ✅ | ❌ | **MISSING from API** |
| `skipRhPrefix` | ✅ | ❌ | **MISSING from API** |
| `skipRhSuffix` | ✅ | ❌ | **MISSING from API** |
| `unmapForGtpHubInfo` | ✅ | ❌ | **MISSING from API** |
| `unodeRulesetName` | ✅ | ❌ | **MISSING from API** |
| `userSupplied` | ✅ | ❌ | **MISSING from API** |
| `ussdDcsRewrite` | ✅ | ❌ | **MISSING from API** |

### Summary: Customer Profile

**Fields available from API:** Only 3 out of 27 fields
- `customerProfileName` (maps to `profileName`)
- `hssRealm`
- `hssHost`

**Fields MISSING from API (present in JSON):** 24 fields
- `imsRealm` - **CRITICAL** - Used extensively in cx-proxy for IMS operations
- `smscNumber` - SMS center configuration
- `mgtPrefix`, `mgtDigitsToReplace`, `useMgtRouting` - MGT routing configuration
- All other profile configuration fields

---

## Implementation Implications

### Critical Issues

1. **No Customer Profile API Endpoint**
   - The API only provides minimal customer profile data embedded in IMSI mapping responses
   - Most customer profile fields are **NOT available** via REST API

2. **Missing Critical Field: `imsRealm`**
   - The current `cx-proxy-local.py` code heavily relies on `customerProfile.imsRealm`
   - Used in lines: 287, 288, 335, 337, 353, 413, 414, 417, 489
   - **This field is NOT provided by the REST API**

3. **Missing Field: `smscNumber`**
   - Used for SMS routing configuration
   - Not available in API

### Recommended Solutions

#### Option 1: Hybrid Approach (Recommended)
- Use REST API for IMSI mapping lookups (benefits from caching)
- Continue using local JSON file for customer profiles (complete data)
- REST API response includes `customerProfileName` which can be used to lookup the full profile locally

**Advantages:**
- Leverages REST API for frequently-changing IMSI mappings
- Maintains access to complete customer profile configuration
- Minimal code changes required

**Implementation:**
```python
# Fetch IMSI mapping from REST API (with caching)
mapping = await rest_client.get_imsi_mapping(sponsored_imsi)

# Use customerProfileName to lookup full profile from local JSON
profile = profile_manager.get_profile_by_name(mapping.customerProfileName)

# Now have access to both mapping and complete profile including imsRealm
```

#### Option 2: Local Augmentation
- Fetch from REST API
- Augment API response with missing fields from local JSON configuration
- Merge data based on `customerProfileName`

#### Option 3: API Enhancement (requires backend changes)
- Request REST API provider to add customer profile endpoint
- Or enhance `/v1/queryMapping` response to include all customer profile fields

---

## Caching Strategy Recommendation

Given the field differences:

1. **Cache IMSI Mapping API Responses** (high priority)
   - Frequently queried
   - Contains more data than local JSON
   - Short TTL recommended (5-15 minutes) as mappings may change

2. **Cache Customer Profile Data** (lower priority)
   - If using hybrid approach, cache the merged result (API mapping + local profile)
   - Longer TTL acceptable (30-60 minutes) as profiles change infrequently

3. **Cache Key Strategy**
   - IMSI Mapping: Cache by `sponsoredImsi`
   - Merged Data: Cache by `sponsoredImsi` with combined mapping+profile object
