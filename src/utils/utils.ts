function getUUID() {
  const str = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx';
  return str.replace(/[xy]/g, item => {
    const r = Math.random() * 0x10 | 0;
    const v = item === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(0x10);
  });
}

function rounded(inputNum: number | null | string | undefined, digital: number): number {
  if (inputNum === null || inputNum === undefined) {
    return 0;
  } else {
    return Math.round(Number(inputNum) * Math.pow(10, digital)) / Math.pow(10, digital);
  }
}

function getUsageColorClass(
  usage: number | undefined | null,
  freeUsageThreshold: number,
  midUsageThreshold: number
): string {
  if (usage === null || usage === undefined) {
    return 'max-color';
  } else {
    if (usage <= freeUsageThreshold) {
      return 'free-color';
    } else if (usage <= midUsageThreshold) {
      return 'mid-color';
    } else {
      return 'max-color';
    }
  }
}

export {
  getUUID,
  rounded,
  getUsageColorClass
};
