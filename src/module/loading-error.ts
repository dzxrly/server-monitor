export class LoadingError {
  public cpuStateFetchError = false;
  public cpuNameFetchError = false;
  public memoryStateFetchError = false;
  public gpuStateFetchError = false;
  public osInfoFetchError = false;

  public hasError(): boolean {
    return (
      this.cpuStateFetchError ||
      this.cpuNameFetchError ||
      this.memoryStateFetchError ||
      this.gpuStateFetchError ||
      this.osInfoFetchError
    );
  }
}
