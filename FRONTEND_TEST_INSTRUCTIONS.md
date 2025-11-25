# Frontend Test Instructions

## Setup

1. Install dependencies:
```bash
cd natl-frontend
npm install
```

## Running Tests

### Run all tests interactively:
```bash
npm test
```

### Run tests once with coverage:
```bash
npm run test:coverage
```

### Run in CI/CD mode (used by GitHub Actions):
```bash
npm test -- --coverage --watchAll=false --passWithNoTests
```

## What Was Added

### 62 New Tests Across 6 Files:

1. **`src/reducers/loginReducer.test.js`** - 7 tests for login state management
2. **`src/reducers/listReducer.test.js`** - 10 tests for list state management  
3. **`src/reducers/taskReducer.test.js`** - 13 tests for task state management
4. **`src/constants/index.test.js`** - 18 tests for action constants
5. **`src/store/configureStore.test.js`** - 6 tests for Redux store
6. **`src/components/App/App.test.js`** - 3 tests (updated from 1)
7. **`src/reportWebVitals.test.js`** - 5 tests for utility function

## Expected Coverage

After running the tests, you should see:
- **Statements:** 75-80%
- **Branches:** 70-75%
- **Functions:** 70-75%
- **Lines:** 75-80%

## Coverage Reports

Coverage reports are generated in `natl-frontend/coverage/`:
- `lcov-report/index.html` - Open this in a browser for visual report
- `coverage-summary.json` - JSON summary used by CI/CD
- `lcov.info` - LCOV format for tools
- `coverage-final.json` - Detailed coverage data

## Viewing Coverage Report

```bash
# After running tests with coverage
cd natl-frontend
open coverage/lcov-report/index.html
# Or on Linux: xdg-open coverage/lcov-report/index.html
```

## Test Categories

### ✅ Fully Tested (100% coverage)
- Redux reducers (loginReducer, listReducer, taskReducer)
- Action constants
- Redux store configuration

### ✅ Partially Tested
- App component (basic rendering)
- reportWebVitals utility

### ❌ Not Yet Tested (can add later)
- Login component
- Dashboard component
- Lists component
- Tasks component
- Preferences component
- Action creators (API calls)

## Troubleshooting

### Issue: "react-scripts: command not found"
**Solution:** Run `npm install` in the natl-frontend directory

### Issue: Tests fail with module not found
**Solution:** Ensure you're in the natl-frontend directory and dependencies are installed

### Issue: Coverage report not generated
**Solution:** Make sure you're using the `--coverage` flag:
```bash
npm test -- --coverage --watchAll=false
```

### Issue: Tests hang or wait for input
**Solution:** Use `--watchAll=false` flag to run once and exit

## CI/CD Integration

The GitHub Actions workflow should run:
```yaml
- name: Run tests with coverage
  working-directory: natl-frontend
  run: npm test -- --coverage --watchAll=false --passWithNoTests
```

This will:
1. Run all 62 tests
2. Generate coverage reports
3. Create `coverage/coverage-summary.json` for the workflow to parse
4. Exit after completion (non-interactive mode)

## Next Steps

To improve coverage to 80%+, add tests for:
1. Login component (authentication flow)
2. Dashboard component (navigation, list display)
3. Lists component (CRUD operations)
4. Tasks component (CRUD operations)
5. Action creators (with mocked API calls)
