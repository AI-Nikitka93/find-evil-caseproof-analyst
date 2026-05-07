# Canonical Investigation Flow

Purpose: define the default autonomous investigation path for CaseProof Analyst
without turning the agent into a broad DFIR shell.

## Flow

1. Open case read-only.
   - Register the evidence path.
   - Create or use the case workspace.
   - Confirm original evidence is input-only.

2. Establish evidence context.
   - Identify the evidence ID.
   - Record case ID, workspace, hash status, and parser status.
   - Stop if the evidence path is missing, unsafe, or not usable.

3. Gather artifact families.
   - List partitions.
   - Gather filesystem inventory.
   - Build bounded timeline context.
   - Extract registry persistence where hives are available.
   - Extract event records where event logs are available.

4. Draft candidate claims.
   - Name the artifact family.
   - State the observed fact.
   - Name the expected evidence reference.
   - Select a confidence target.

5. Verify every candidate claim.
   - Run `verify_claim`.
   - Keep linked supporting evidence for confirmed findings.
   - Downgrade or drop weak claims.
   - Send missing, ambiguous, or conflicted claims to human review.

6. Correct or downgrade.
   - If parser failure, evidence conflict, unsafe request, or unsupported claim
     appears, record the correction event.
   - Run only bounded follow-up checks.
   - Do not retry indefinitely.

7. Report.
   - Confirmed findings include evidence and tool trace.
   - Inferred findings name limitations.
   - Unsupported dropped claims remain visible.
   - Correction ledger records what changed and why.

## Stop Conditions

- Required evidence is missing.
- Required SIFT tools are missing.
- The next step would require broad shell access.
- The next step would mutate original evidence.
- Tool-call or iteration budget is exhausted.
- Remaining claims cannot be supported without guessing.
