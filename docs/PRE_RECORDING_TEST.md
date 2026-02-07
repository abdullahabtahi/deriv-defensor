# ✅ Pre-Recording Test Checklist

Run through this BEFORE you hit record. Takes 3 minutes, saves you from re-recording.

---

## 🚀 STEP 1: Start the Dashboard

```bash
cd "/Users/abdullahabtahi/deriv defensor"
source .venv_final/bin/activate
streamlit run dashboard/app.py
```

**Expected:** Dashboard opens at http://localhost:8501

✅ Dashboard loads without errors
✅ All metrics display correctly
✅ No red error messages

---

## 🔍 STEP 2: Test All Pages (Click Each One)

### Home (Command Center)
- [ ] 4 headline metrics load
- [ ] Regional risk chart displays
- [ ] Contagion alerts show (if any)
- [ ] Live feed shows 5 partners

### Page 0: Business Impact
- [ ] 3 headline cards (Risk Exposure, Recoverable, ROI)
- [ ] Business Impact Table loads
- [ ] EMPC calculation visible
- [ ] Waterfall chart renders
- [ ] Scenario simulator sliders work

### Page 1: ROI Deep Dive
- [ ] Headline ROI card (gradient background)
- [ ] Profit comparison bar chart
- [ ] Cumulative profit curve
- [ ] Sliders adjust calculations

### Page 2: Intervention Log
- [ ] Intervention history table populated
- [ ] Success rate metrics display
- [ ] Charts render

### Page 3: Agent Control
- [ ] Settings panel visible
- [ ] Can toggle automation
- [ ] Guardrails section loads

### Page 4: CRM Integration
- [ ] Mock CRM panel
- [ ] Task list shows

### Page 5: Partner Analysis
- [ ] Search bar works
- [ ] Can select partner
- [ ] Risk score displays
- [ ] Charts load

### Page 6: Alert Monitor
- [ ] Alerts table populated
- [ ] Can acknowledge alerts

### Page 7: Pattern Discovery
- [ ] Top discovery card shows
- [ ] Synergy bar chart renders
- [ ] Pattern detail table loads
- [ ] Interaction heatmap displays
- [ ] Deep dive visualization works

---

## 🎯 STEP 3: Test Critical Demo Path

**This is your exact presentation flow. Test it!**

### 3.1: Business Impact Demo
1. Navigate to **Business Impact** (Page 0)
2. Wait 2 seconds for load
3. Scroll to Business Impact Table
4. Scroll to Waterfall Chart
5. **Check:** All numbers visible and correct?

✅ Passes visual test

---

### 3.2: Pattern Discovery Demo
1. Navigate to **Pattern Discovery** (Page 7)
2. Wait 2 seconds for load
3. Note the top pattern synergy %
4. Scroll to comparison chart
5. **Check:** 83% vs 36% bars visible?

✅ Top pattern shows correctly

---

### 3.3: Live Intervention Demo (CRITICAL!)

**This is your wow moment. Test thoroughly.**

1. Go to **Command Center** (Home)
2. Find Partner P00001 in the feed or search
   - If not visible, check dataset has P00001
3. Click Partner P00001
4. Partner Analysis page loads
5. Scroll to risk score section
6. **Check GenAI component if enabled:**
   - Does explanation generate?
   - Does email draft show?
   - Does it make sense?

✅ P00001 loads correctly
✅ Risk score is high (>80%)
✅ GenAI explanation works (or screenshot ready)

---

## 🎨 STEP 4: Visual Polish Check

Open each page and ask:
- Are colors correct? (no ugly defaults)
- Are numbers formatted? (not 32000000.123)
- Are charts labeled?
- Is text readable?
- Any console errors? (F12 to check)

✅ Dashboard looks professional

---

## 🔊 STEP 5: Audio Test

Record 15 seconds of test audio:

1. Start recording tool (Loom/OBS/QuickTime)
2. Say: "Testing audio. The quick brown fox jumps over the lazy dog."
3. Stop recording
4. Play back

**Check:**
- [ ] Audio is clear (no static)
- [ ] Volume is good (not too quiet)
- [ ] No background noise
- [ ] No echo

✅ Audio quality approved

---

## 🖥️ STEP 6: Screen Recording Test

Record 30 seconds of dashboard interaction:

1. Start screen recording
2. Navigate: Home → Business Impact → Pattern Discovery
3. Stop recording
4. Play back

**Check:**
- [ ] Resolution is clear (1080p)
- [ ] Cursor is visible
- [ ] Scrolling is smooth (not choppy)
- [ ] Frame rate is good (30fps+)
- [ ] Browser UI is clean (no extra tabs)

✅ Screen recording quality approved

---

## 📋 STEP 7: Environment Cleanup

### Browser
- [ ] Close all other tabs
- [ ] Hide bookmarks bar
- [ ] Full screen mode (F11 or Cmd+Ctrl+F)
- [ ] Zoom to 100%
- [ ] Clear console errors

### Desktop
- [ ] Close unnecessary apps
- [ ] Hide desktop icons (if showing)
- [ ] Disable notifications (macOS: Option+Click notification icon)
- [ ] Turn off Slack/Discord
- [ ] Close email client

### Recording Area
- [ ] Dashboard fills screen
- [ ] No distractions in frame
- [ ] Lighting is good (if camera on)

✅ Clean environment

---

## 🎤 STEP 8: Final Script Check

Read your script OUT LOUD once:

1. Open [PRESENTATION_CHEAT_SHEET.md](PRESENTATION_CHEAT_SHEET.md)
2. Read opening hook (0:00-0:45)
3. Read closing punch (4:15-4:45)
4. Time yourself

**Check:**
- [ ] You're not rushing
- [ ] You're emphasizing key numbers (5x, $32M, 67%)
- [ ] You're pausing before big reveals
- [ ] It feels natural (not robotic)

✅ Script rehearsed

---

## 🚨 CRITICAL DEMO ELEMENTS CHECK

Before recording, verify these are ready:

### Data
- [ ] 10,000 partners in dataset
- [ ] Partner P00001 exists
- [ ] Churn rate ~20%
- [ ] High-risk partners visible in feed

### Metrics
- [ ] ROI shows 5.0x+ improvement
- [ ] Partners saved: 172 (AI) vs 127 (random)
- [ ] Pattern synergy: 67%+
- [ ] EMPC profit: $32M+ (AI)

### Features
- [ ] GenAI explainer works (or have screenshot)
- [ ] Charts all render
- [ ] No loading spinners stuck
- [ ] No error modals

✅ All critical elements verified

---

## ⏱️ STEP 9: Timing Dry Run

Do a complete dry run WITHOUT recording:

1. Start timer
2. Navigate through full presentation path
3. Speak the script (can be fast/mumbled)
4. Stop timer

**Target:** 4:00-4:45

- [ ] Under 5:00?
- [ ] Over 4:00?
- [ ] Pacing feels right?

✅ Timing on track

---

## 🎬 STEP 10: You're Ready!

If all boxes are checked, you're good to record.

### Final Mental Checklist:
- [ ] Water nearby
- [ ] Bathroom break taken
- [ ] Phone on silent
- [ ] Script visible (off-camera)
- [ ] Deep breath
- [ ] Confident mindset

### Recording Tips:
1. **Count down:** "Recording in 3... 2... 1..."
2. **Pause 2 seconds** before speaking (easier to edit)
3. **If you mess up:** Pause, take breath, restart THAT section
4. **Don't stop for minor stumbles** - keep energy up
5. **Finish strong** - even if earlier parts were rough

---

## 🚀 BACKUP PLANS

### If Dashboard Breaks
- [ ] Have Railway URL ready
- [ ] Screenshot critical pages
- [ ] Narrate over screenshots

### If You Run Over Time
Priority cuts (see [PRESENTATION_CHEAT_SHEET.md](PRESENTATION_CHEAT_SHEET.md))

### If GenAI Doesn't Work Live
- [ ] Pre-recorded GenAI output as screenshot
- [ ] Say: "Here's the AI explanation [show image]"

---

## 📊 POST-RECORDING CHECKLIST

After you record, before you submit:

- [ ] Total length < 5:00
- [ ] Audio is clear throughout
- [ ] All key metrics are visible
- [ ] No awkward pauses/cuts
- [ ] Ending is strong
- [ ] Export quality: 1080p MP4
- [ ] File size < 500MB (for upload)

---

## 🎯 QUALITY GATES

**Don't submit if:**
- ❌ Over 5:00 (disqualified!)
- ❌ Audio is inaudible
- ❌ Screen is blurry
- ❌ Demo obviously broken
- ❌ Missing 5x ROI number

**It's OK if:**
- ✅ You stutter a bit (shows authenticity)
- ✅ You're under 4:00 (brevity is good!)
- ✅ You use Railway instead of local
- ✅ You skip one non-critical page

---

## 💪 FINAL PEP TALK

You built something complete. The numbers are real. The demo works.

**You got this! 🚀**

Now go record that winning presentation.

Remember: Confidence is contagious. If you believe in it, they will too.

---

**LAST STEP:** Check this box when you're 100% ready

- [ ] I've tested everything. I'm ready to record. Let's go! 🎬
