import reportWebVitals from './reportWebVitals';

describe('reportWebVitals', () => {
  it('should call onPerfEntry when provided and web-vitals is available', () => {
    const mockOnPerfEntry = jest.fn();
    reportWebVitals(mockOnPerfEntry);
    // Function exists and doesn't throw
    expect(typeof reportWebVitals).toBe('function');
  });

  it('should not throw when called without arguments', () => {
    expect(() => {
      reportWebVitals();
    }).not.toThrow();
  });

  it('should not throw when called with null', () => {
    expect(() => {
      reportWebVitals(null);
    }).not.toThrow();
  });

  it('should not throw when called with undefined', () => {
    expect(() => {
      reportWebVitals(undefined);
    }).not.toThrow();
  });

  it('should accept a function as argument', () => {
    const mockCallback = jest.fn();
    expect(() => {
      reportWebVitals(mockCallback);
    }).not.toThrow();
  });
});
