// This is just an example,
// so you can safely delete all default props below

export default {
  NVIDIA: 'NVIDIA',
  AMD: 'AMD',
  INTEL: 'Intel',
  NoneGPU: 'No GPU',

  cancelBtn: 'Cancel',
  confirmBtn: 'Confirm',
  addBtn: 'Add',
  addServer: 'Add Server',
  serverUUID: 'Server UUID',
  customServerName: 'Custom Server Name',
  customServerNameInputFieldHint: '1~16 characters',
  customServerNameInputFieldHintErrorMsg:
    'Input length muse be in 1~16 characters',
  serverUrl: 'Server URL',
  serverUrlInputFieldHint: 'Server URL can not be NULL',
  serverUrlInputFieldHintErrorMsg: "Please input your server's URL",
  serverTagColor: 'Server Tag Color',
  serverTagColorHint: "Server's tag color can not be NULL",
  serverTagColorHintErrorMsg: "Please choose your server's tag color",
  serverGPUType: 'Server GPU Type',

  usage: 'Usage',
  cpuUsage: 'CPU Usage',
  cpuInfo: 'CPU Information',
  cpuFreq: 'CPU Frequency',
  cpuTemp: 'CPU Temperature',
  memoryUsage: 'RAM Usage',
  swapUsage: 'Swap Usage',
  gpuUsage: 'GPU Usage',
  loadingFailed: 'Loading failed',
  loadingFailedTooltip: 'Loading failed, please check your network connection',
  gpuDriverVersion: 'Driver Ver.',
  gpuInfo: 'GPU Information',
  gpuCoreUsage: 'GPU Load',
  gpuMemoryUsage: 'VRAM Usage',
  degreeC: '°C',
  degreeF: '°F',
  power: 'Power',
  fanSpeed: 'Fan Speed',
  core: 'Core',
  maxTemperature: 'Max Temperature',
  currentTemperature: 'Current Temperature',
  criticalTemperature: 'Critical Temperature',
  rowsPerPage: 'Rows Per Page',
  memoryAndSwap: 'Memory and Swap',
  memoryUnit: 'Memory Unit',
  gpuMemoryUnit: 'VRAM Unit',

  settings: 'Settings',
  darkMode: 'Dark Mode',
  useFahrenheitUnit: 'Use Fahrenheit Unit',
  indexPageServerPanelLayout: 'Server Panel Layout',
  layoutSm: 'Dense Layout',
  layoutMd: 'Normal Layout',
  layoutLg: 'Details Layout',
  language: 'Language',
  settingsSaved: 'Settings saved',
  refreshTimeSec: 'Data Refresh Time (sec)',
  freeUsageThreshold: 'Free Usage Threshold %',
  midUsageThreshold: 'Mid Usage Threshold %',
  resetSettingBtn: 'Reset',
  resetSettingConfirmTitle: 'Reset Settings',
  resetSettingConfirm:
    'Are you sure to reset all settings? This action can not be undone!',
  resetSettingSuccess: 'Settings reset successfully',
  exportSettingBtn: 'Export',
  importSettingBtn: 'Import',
  importSettingSuccess: 'Settings imported successfully',
  importSettingFail: 'Import settings failed',
  importSettingFailNotAConfigFile:
    'Import settings failed! This is not a valid config file',
  importSettingFailNoFile: 'Import settings failed! No file to import',
  importSettingFailDuplicateUniqueId:
    'Import settings failed! Duplicate server UUID or UUID error',

  serverRouteFailed: 'Open server details failed, there is not server: ',
  serverNotFound: 'Server not found',
  deleteThisServer: 'Delete Server',
  deleteThisServerConfirm:
    'Are you sure to delete this server? This action can not be undone!',
  serverDeleted: 'Server Deleted',
  numaNode: 'NUMA Node',
  serverSettings: 'Server Settings',
  serverEditDialogSaveErrorMsg:
    'Server information error, please check your inputs',
  saveEditBtn: 'Save',

  sourceCode: 'Project Repo',
  privacyPolicy: 'Privacy Policy',
  backendDeployTitle: 'Server Monitor Backend',
  backendDeployDesc:
    'To use Server Monitor to monitor the server hardware, you need to deploy the corresponding backend in the server first, please refer to the ',
  noPopupTips: "Don't remind me again",
  backendDeployDocs: 'Server Monitor Backend Documents',
};
