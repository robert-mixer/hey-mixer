# Handoff Adapters

<!-- PURPOSE: Future integration with researcher agent -->
<!-- STATUS: Placeholder for future enhancement -->
<!-- PRIORITY: Not required for MVP -->

## Overview

This directory is reserved for future integration with a "researcher agent" that can perform deep analysis of GitHub issues before goal creation.

## Planned Architecture

### Request Schema (schema.request.json)

The goal-builder would send requests to the researcher agent with:
- GitHub issue numbers
- Analysis depth required
- Specific questions to research
- Context about the codebase

### Response Schema (schema.response.json)

The researcher agent would return:
- Detailed analysis of issues
- Suggested groupings with rationale
- Technical feasibility assessment
- Recommended approach
- Potential risks identified
- Related codebase areas

## Current Status

**Not implemented.** The goal-builder currently works directly with GitHub and Linear APIs via MCP servers.

## Future Use Case

**Scenario**: User has 50+ open GitHub issues and wants intelligent grouping suggestions.

**Without Researcher**:
- Goal-builder lists all issues
- Agent suggests groupings based on titles/descriptions
- Limited depth of analysis

**With Researcher**:
- Goal-builder delegates to researcher agent
- Researcher performs deep analysis:
  - Reads full issue content
  - Analyzes code references
  - Checks dependencies
  - Assesses complexity
  - Identifies patterns
- Researcher returns structured recommendations
- Goal-builder presents enhanced groupings to user

## Implementation Notes

When this is eventually implemented:

1. **Communication Protocol**: Could use file-based handoff or direct API
2. **Async Operation**: Researcher may take time for deep analysis
3. **Feedback Loop**: User can refine researcher's suggestions
4. **Command Integration**: Add dedicated slash command to delegate to researcher

## Delegation Configuration (Future)

```yaml
researcher:
  description: "Deep analysis of GitHub issues before goal creation"
  enabled: false  # Not yet implemented
  analysis_depth: "comprehensive"
  timeout: 300  # seconds
  use_cases:
    - Large number of issues (50+)
    - Complex domain requiring analysis
    - Uncertain about groupings
    - Need technical feasibility assessment
```

## Related Files

- `schema.request.json` - (Future) Request format to researcher
- `schema.response.json` - (Future) Response format from researcher

## For Now

The goal-builder works without the researcher agent using:
- Direct MCP access to GitHub issues
- Agent's own analysis capabilities
- Interactive collaboration with user

This handoff system can be added later without changing core workflows.
