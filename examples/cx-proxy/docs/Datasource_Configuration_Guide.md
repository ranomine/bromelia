# Datasource Configuration Guide

This guide explains how to configure the CX Proxy to use different data sources for IMSI mappings and customer profiles.

## Configuration File

The datasource behavior is controlled by `config/datasource.conf`.

## Configuration Modes

### 1. JSON Mode (File-based)
Uses local JSON files for all data.

```ini
[datasource]
mode = json

[imsi_mapping]
source = json
json_file = ./config/imsi_mappings.json

[customer_profile]
source = json
json_file = ./config/customer_profiles.json
```

**Pros:**
- Fast, no network latency
- Always available (no REST API dependency)
- Complete customer profile data

**Cons:**
- Requires manual updates to JSON files
- No real-time updates
- Needs application restart to reload changes

**Use case:** Development, testing, or standalone deployments

---

### 2. REST Mode (API-based)
Fetches data from external REST API.

```ini
[datasource]
mode = rest
cache_enabled = true

[imsi_mapping]
source = rest
rest_base_url = http://api.example.com:1705
rest_timeout = 5.0

[customer_profile]
source = json  # Still use JSON - REST API missing critical fields
json_file = ./config/customer_profiles.json
```

**Pros:**
- Real-time data updates
- Centralized data management
- No need to update local files

**Cons:**
- Network latency
- REST API must be available
- Missing customer profile fields (see API_vs_JSON_Comparison.md)

**Use case:** Production deployments with centralized IMSI mapping service

---

### 3. Hybrid Mode (REST with JSON Fallback)
Uses REST API but falls back to JSON files if API is unavailable.

```ini
[datasource]
mode = hybrid
cache_enabled = true

[imsi_mapping]
source = rest
json_file = ./config/imsi_mappings.json
rest_base_url = http://api.example.com:1705
fallback_on_rest_failure = json

[customer_profile]
source = json
json_file = ./config/customer_profiles.json
```

**Pros:**
- Best of both worlds
- High availability (works even if REST API is down)
- Real-time updates when API is available
- Graceful degradation

**Cons:**
- Slightly more complex configuration
- Need to maintain both JSON files and REST API access

**Use case:** Production deployments requiring high availability

---

## Caching Configuration

### Cache TTL (Time-to-Live)

Controls how long cached data remains valid:

```ini
[cache]
imsi_mapping_ttl = 300        # 5 minutes
customer_profile_ttl = 1800   # 30 minutes
```

**Recommendations:**
- **IMSI Mappings:** 300-900 seconds (5-15 minutes)
  - Mappings may change frequently
  - Balance between API load and data freshness

- **Customer Profiles:** 1800-3600 seconds (30-60 minutes)
  - Profiles change infrequently
  - Can use longer TTL

### Cache Size Management

```ini
[cache]
max_cache_size = 10000        # Maximum 10,000 entries
cleanup_interval = 60         # Clean up every 60 seconds
```

**Memory estimation:**
- Each IMSI mapping entry: ~1-2 KB
- 10,000 entries ≈ 10-20 MB memory
- Adjust based on your traffic and available memory

### LRU Eviction

When `max_cache_size` is reached, the Least Recently Used (LRU) entries are evicted automatically.

---

## REST API Configuration

### Connection Settings

```ini
[imsi_mapping]
rest_base_url = http://localhost:1705
rest_endpoint = /v1/queryMapping/{sponsoredImsi}
rest_timeout = 5.0            # Request timeout in seconds
rest_retry_attempts = 3       # Number of retries on failure
rest_retry_delay = 1.0        # Delay between retries (seconds)
```

### Timeout Recommendations

- **Low-latency network (same datacenter):** 2-5 seconds
- **High-latency network (internet):** 10-15 seconds
- **Critical path:** Use lower timeout + JSON fallback

### Retry Strategy

The implementation uses **exponential backoff**:
- Attempt 1: immediate
- Attempt 2: after 1 second
- Attempt 3: after 2 seconds
- Attempt 4: after 4 seconds

---

## Fallback Behavior

Controls what happens when REST API fails:

```ini
[imsi_mapping]
fallback_on_rest_failure = json  # Options: json, none, error
```

### Fallback Options

1. **`json`** (Recommended for hybrid mode)
   - On REST failure, load from JSON file
   - Logs warning but continues operation
   - Ensures high availability

2. **`none`**
   - On REST failure, return None
   - Application must handle None values
   - Useful for testing REST API connectivity

3. **`error`**
   - On REST failure, raise exception
   - Application will fail/crash
   - Useful for strict production deployments where stale data is unacceptable

---

## Example Configurations

### Example 1: Development (JSON only)

```ini
[datasource]
mode = json
cache_enabled = false

[imsi_mapping]
source = json
json_file = ./config/imsi_mappings.json

[customer_profile]
source = json
json_file = ./config/customer_profiles.json
```

Fast startup, no dependencies, easy testing.

---

### Example 2: Production (Hybrid with caching)

```ini
[datasource]
mode = hybrid
cache_enabled = true

[imsi_mapping]
source = rest
json_file = ./config/imsi_mappings.json
rest_base_url = http://imsi-api.internal:1705
rest_timeout = 3.0
rest_retry_attempts = 2
fallback_on_rest_failure = json

[customer_profile]
source = json
json_file = ./config/customer_profiles.json

[cache]
imsi_mapping_ttl = 600
customer_profile_ttl = 3600
max_cache_size = 50000
cleanup_interval = 300

[logging]
log_cache_hits = false
log_cache_misses = true
log_rest_calls = true
```

High availability, good performance, detailed logging of issues.

---

### Example 3: Pure REST (when API has complete data)

```ini
[datasource]
mode = rest
cache_enabled = true

[imsi_mapping]
source = rest
rest_base_url = http://imsi-api.internal:1705
rest_timeout = 5.0
fallback_on_rest_failure = error

[customer_profile]
source = rest
rest_base_url = http://profile-api.internal:1705
rest_timeout = 5.0
fallback_on_rest_failure = error

[cache]
imsi_mapping_ttl = 300
customer_profile_ttl = 1800
```

**Note:** Only use this if your REST API provides ALL customer profile fields (currently it doesn't - see API_vs_JSON_Comparison.md).

---

## Migration Path

### From JSON to Hybrid

1. Keep existing JSON files
2. Set up REST API access
3. Update `datasource.conf`:
   ```ini
   [imsi_mapping]
   source = rest
   fallback_on_rest_failure = json
   ```
4. Test thoroughly
5. Monitor logs for fallback occurrences

### From Hybrid to REST

1. Ensure REST API is stable
2. Verify all required fields are available
3. Update configuration:
   ```ini
   [imsi_mapping]
   fallback_on_rest_failure = error
   ```
4. Monitor for errors
5. Once stable, optionally remove JSON files (keep as backup)

---

## Monitoring and Troubleshooting

### Cache Statistics

Enable cache statistics to monitor performance:

```ini
[logging]
cache_stats_enabled = true
cache_stats_interval = 300  # Log stats every 5 minutes
```

Example log output:
```
[INFO] Cache stats: IMSI Mapping - Hits: 8543, Misses: 234, Hit Rate: 97.3%, Size: 1247/10000
[INFO] Cache stats: Customer Profile - Hits: 423, Misses: 12, Hit Rate: 97.2%, Size: 45/10000
```

### REST API Health Checks

Monitor these log messages:

```
[WARNING] REST API call failed for IMSI 234106479730357, falling back to JSON
[ERROR] REST API unavailable, using JSON fallback exclusively
[INFO] REST API recovered, resuming REST mode
```

### Common Issues

**Issue:** High cache miss rate
- **Solution:** Increase `imsi_mapping_ttl`

**Issue:** Memory usage growing
- **Solution:** Reduce `max_cache_size` or implement cleanup

**Issue:** REST API timeouts
- **Solution:** Increase `rest_timeout` or reduce `rest_retry_attempts`

**Issue:** Stale data
- **Solution:** Reduce TTL values or implement cache invalidation

---

## Performance Tuning

### High-Traffic Deployments

```ini
[cache]
imsi_mapping_ttl = 900        # 15 minutes
max_cache_size = 100000       # 100K entries ≈ 100-200 MB RAM
cleanup_interval = 600        # Clean up every 10 minutes

[imsi_mapping]
rest_timeout = 2.0            # Aggressive timeout
rest_retry_attempts = 1       # Single retry only
```

### Low-Traffic Deployments

```ini
[cache]
imsi_mapping_ttl = 300        # 5 minutes
max_cache_size = 1000         # Small cache
cleanup_interval = 60         # Frequent cleanup

[imsi_mapping]
rest_timeout = 10.0           # Patient timeout
rest_retry_attempts = 5       # Multiple retries
```

---

## Security Considerations

### REST API Authentication

If your REST API requires authentication, extend the configuration:

```ini
[imsi_mapping]
rest_base_url = https://secure-api.example.com:1705
rest_auth_type = bearer
rest_auth_token_file = ./config/api_token.secret

# Or for basic auth:
# rest_auth_type = basic
# rest_auth_username = api_user
# rest_auth_password_file = ./config/api_password.secret
```

### TLS/SSL

Always use HTTPS in production:

```ini
[imsi_mapping]
rest_base_url = https://api.example.com:1705
rest_verify_ssl = true
rest_ca_bundle = /etc/ssl/certs/ca-bundle.crt
```

---

## Testing Configuration Changes

Before deploying configuration changes:

1. **Validate config file syntax:**
   ```bash
   python3 -c "import configparser; c=configparser.ConfigParser(); c.read('config/datasource.conf')"
   ```

2. **Test REST API connectivity:**
   ```bash
   curl -v http://localhost:1705/v1/queryMapping/234106479730357
   ```

3. **Dry run with logging:**
   ```ini
   [logging]
   log_cache_hits = true
   log_cache_misses = true
   log_rest_calls = true
   log_json_loads = true
   ```

4. **Monitor application logs during initial rollout**

---

## Best Practices

1. ✅ **Always configure fallback** in production (use hybrid mode)
2. ✅ **Enable caching** to reduce API load
3. ✅ **Monitor cache hit rates** to tune TTL values
4. ✅ **Keep JSON files updated** as backup datasource
5. ✅ **Use appropriate timeouts** based on network conditions
6. ✅ **Log REST failures** to detect API issues early
7. ✅ **Test configuration** in staging before production
8. ✅ **Document any customizations** specific to your deployment
