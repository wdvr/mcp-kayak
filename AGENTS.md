# Development Rules

This repository follows the guidelines below for all contributions:

- If an API key is required, use an environment variable and document it.
- Maintain a `PLAN.txt` file summarizing current tasks and linking to the corresponding GitHub issues. Update this file alongside the issues whenever work progresses.
- Keep code concise and remove unused code before committing.
- Use typed Python where possible.
- Before committing, ensure linting and cleanup are performed. No lingering code should remain.
- Write tests that provide value without excess. Use GitHub workflows to run tests on shared runners.
- Always run the test suite and ensure all tests pass before opening a pull request.
- To interact with GitHub programmatically (e.g., creating issues), configure the environment variable `GITHUB_TOKEN` or `GH_TOKEN` with appropriate permissions.
 - An example `curl` call for creating issues is documented in the README.
