# Multi-Key Setup Guide

## ✅ Multi-Key API System Installed!

You now have automatic key rotation that switches between multiple Groq API keys when rate limits are hit.

---

## 🔑 How to Add Multiple Keys

### Step 1: Get Additional API Keys

1. Go to: https://console.groq.com/keys
2. Click "Create API Key"
3. Name it (e.g., "Key 2", "Key 3")
4. Copy the key (starts with `gsk_...`)
5. Repeat for as many keys as you want (up to 9 supported)

### Step 2: Add Keys to `.env` File

Open your `.env` file and add the new keys:

```bash
# Primary key (already exists)
GROQ_API_KEY=gsk_your_primary_key_here

# Add secondary keys
GROQ_API_KEY_2=gsk_your_second_key_here
GROQ_API_KEY_3=gsk_your_third_key_here
# ... up to GROQ_API_KEY_9
```

**Important**: 
- Keep the same format: `GROQ_API_KEY_2`, `GROQ_API_KEY_3`, etc.
- No spaces around the `=` sign
- One key per line

### Step 3: Test the Setup

Run this to verify all keys are loaded:

```bash
python utils/groq_key_manager.py
```

You should see:
```
✅ Loaded 3 Groq API key(s)
   - GROQ_API_KEY
   - GROQ_API_KEY_2
   - GROQ_API_KEY_3
```

---

## 📊 Capacity with Multiple Keys

| Keys | Requests/Minute | Requests/Day | Multi-Year Dataset |
|------|-----------------|--------------|-------------------|
| 1 key | 30 | 14,400 | ⚠️  Tight |
| 2 keys | 60 | 28,800 | ✅ Comfortable |
| 3 keys | 90 | 43,200 | ✅ Plenty |
| 4 keys | 120 | 57,600 | ✅ Overkill |

**For Multi-Year Validation (Enhancement 2):**
- Need: ~1,800 API calls
- With 1 key: Possible but slow (rate limits)
- With 2 keys: Smooth and fast ✅
- With 3+ keys: Very fast ✅

---

## 🔄 How Automatic Rotation Works

1. **System starts with Key 1**
2. **When Key 1 hits rate limit:**
   - System automatically switches to Key 2
   - Prints: `🔄 Rotated to GROQ_API_KEY_2`
3. **When Key 2 hits rate limit:**
   - Switches to Key 3
4. **When all keys are rate-limited:**
   - Waits 60 seconds for cooldown
   - Resumes with Key 1

**You don't need to do anything - it's fully automatic!**

---

## 🚀 Ready to Use

The system is already integrated into:
- ✅ `neural_engine/llm_runner_multikey.py` - Enhanced LLM runner
- ✅ `utils/groq_key_manager.py` - Key management system

**To use multi-key support in future experiments:**

Just import the enhanced runner:
```python
from neural_engine.llm_runner_multikey import analyze_stock
```

Instead of the old one:
```python
from neural_engine.llm_runner import analyze_stock
```

---

## 📝 Current Status

**Keys Loaded**: 1 (GROQ_API_KEY)

**To add more keys:**
1. Get new keys from https://console.groq.com/keys
2. Add to `.env` as `GROQ_API_KEY_2`, `GROQ_API_KEY_3`, etc.
3. Restart your script

**Recommended for Enhancement 2 (Multi-Year Validation):**
- Add at least 1 more key (total 2 keys)
- This will give you 60 requests/minute
- Plenty for smooth multi-year data collection

---

## ✅ Next Steps

**Option A: Add keys now**
1. Go to https://console.groq.com/keys
2. Create 1-2 new keys
3. Add to `.env` file
4. Proceed with Enhancement 2

**Option B: Proceed with current key**
- You can still do Enhancement 2 with 1 key
- It will just be slower (rate limit pauses)
- System will handle it automatically

**What would you like to do?**
