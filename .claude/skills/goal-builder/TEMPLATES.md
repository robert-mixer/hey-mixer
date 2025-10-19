# Goal Ticket Templates

## Feature Implementation Goal

```markdown
# [Feature Name] Implementation

Implement a complete [feature] that provides [core value proposition].

## Requirements

- Core functionality requirement
- User experience requirement
- Performance requirement
- Security requirement
- Integration requirement

## Success Criteria

- Users can [primary action]
- System handles [edge case]
- Performance meets [metric]
- Security passes [standard]
- Integration with [system] works

## Target

`modules/[category]/[feature-name]/` - New [feature] module

## Technical Considerations

- Architecture pattern to use
- Key dependencies
- Performance constraints
- Security requirements

## Related GitHub Issues

- #[number]: [title]
- #[number]: [title]
```

## Bug Fix Collection Goal

```markdown
# [System Area] Bug Fixes and Improvements

Address critical bugs and improvements in the [system area] to enhance stability and user experience.

## Issues to Fix

1. **[Bug Title]** - [Brief description]
2. **[Bug Title]** - [Brief description]
3. **[Improvement]** - [Brief description]

## Success Criteria

- All listed bugs are resolved
- No regression in existing functionality
- Test coverage increased for affected areas
- Performance maintained or improved

## Target

`modules/[existing-module]/` - Updates to existing module

## Testing Requirements

- Unit tests for all fixes
- Integration tests for workflow impacts
- Regression test suite passes

## Related GitHub Issues

- #[number]: [bug title]
- #[number]: [bug title]
```

## Technical Debt Goal

```markdown
# [Component] Refactoring and Modernization

Refactor [component] to improve maintainability, performance, and align with modern best practices.

## Refactoring Scope

- Migrate from [old approach] to [new approach]
- Update dependencies to latest versions
- Improve code organization and structure
- Add comprehensive documentation
- Increase test coverage to [target]%

## Success Criteria

- All existing functionality preserved
- Performance improved by [metric]
- Test coverage at [percentage]
- Documentation complete
- No breaking changes for consumers

## Target

`modules/[component]/` - Refactored module

## Migration Strategy

- Phase 1: [description]
- Phase 2: [description]
- Rollback plan: [description]

## Related GitHub Issues

- #[number]: [tech debt issue]
- #[number]: [modernization request]
```

## Integration Goal

```markdown
# [Service/API] Integration

Integrate with [external service/API] to enable [capability].

## Integration Requirements

- Authentication with [service]
- Data synchronization
- Error handling and retry logic
- Rate limiting compliance
- Monitoring and alerting

## Success Criteria

- Successful authentication flow
- Data syncs reliably
- Graceful error handling
- Respects rate limits
- Monitoring dashboards operational

## Target

`modules/integrations/[service-name]/` - New integration module

## API Endpoints

- Authentication: [endpoint]
- Data operations: [endpoints]
- Webhook handlers: [endpoints]

## Related GitHub Issues

- #[number]: [integration request]
- #[number]: [related feature]
```

## Usage Tips

1. **Don't just copy templates** - Use these as starting points and customize for each goal
2. **Be specific** - Replace placeholders with concrete details
3. **Keep it achievable** - Each goal should be completable in 1-2 sprints
4. **Think modular** - Goals should produce discrete, testable modules
5. **Consider dependencies** - Note what needs to be built first