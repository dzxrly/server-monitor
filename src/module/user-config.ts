class ServerConfig {
  public customName = '';
  public uniqueId = '';
  public serverUrl = '';
  public tagColor = '#000000';
}

class UserConfig {
  public userConfig = {
    darkMode: false,
    defaultLanguage: 'en-US',

    indexPageServerPanelLayout: 'small',

    serverListConfig: Array<ServerConfig>()
  };

  public toString() {
    return JSON.stringify(this.userConfig);
  }

  public fromString(str: string) {
    this.userConfig = JSON.parse(str);
  }
}

export {
  ServerConfig,
  UserConfig
};
