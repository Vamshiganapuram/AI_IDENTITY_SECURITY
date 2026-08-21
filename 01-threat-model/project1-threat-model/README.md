# project1-threat-model

SecureNova Inc. **AI Identity Security** capstone — **Project 1: Threat Model the AI Identity System**.

## What is in this folder

| Path | Purpose |
|------|---------|
| `Project1_Threat_Model_Report.md` | Narrative: identities, trust boundaries, STRIDE, attack trees, ATLAS, ranked risks |
| `SCREENSHOT_PLAYBOOK.md` | Exact 8 screenshots for Mettl (full screen + URL) |
| `deliverables/SecureNova_AI_Identity_ThreatDragon.json` | Import into [OWASP Threat Dragon](https://www.threatdragon.com) |
| `deliverables/AttackTree1_LLM_API_Key_Exfiltration.drawio` | draw.io tree 1 |
| `deliverables/AttackTree2_Agent_Identity_Spoofing.drawio` | draw.io tree 2 |
| `deliverables/AttackTree3_RAG_Chunk_Poisoning.drawio` | draw.io tree 3 |
| `deliverables/STRIDE_Matrix_and_Risk_Register.html` | Open in Excel/browser for screenshots 6–7 |
| `deliverables/*.csv` | Identity inventory, STRIDE matrix, risk register |

## How you submit

1. Take the 8 screenshots in `SCREENSHOT_PLAYBOOK.md`.
2. Paste them into **one Word document** with titles, in order.
3. Export **PDF**.
4. ZIP the PDF and upload to Mettl.

Regenerate files:

```text
python tools/build_deliverables.py
```
