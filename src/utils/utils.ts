import { i18n } from 'src/boot/i18n';

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
  midUsageThreshold: number,
  isText = true
): string {
  if (usage === null || usage === undefined) {
    return isText ? 'text-max-color' : 'bg-max-color';
  } else {
    if (usage <= freeUsageThreshold) {
      return isText ? 'text-free-color' : 'bg-free-color';
    } else if (usage <= midUsageThreshold) {
      return isText ? 'text-mid-color' : 'bg-mid-color';
    } else {
      return isText ? 'text-max-color' : 'bg-max-color';
    }
  }
}

function getUsageColor(
  usage: number | undefined | null,
  freeUsageThreshold: number,
  midUsageThreshold: number
): string {
  if (usage === null || usage === undefined) {
    return getComputedStyle(document.body).getPropertyValue('--max-color');
  } else {
    if (usage <= freeUsageThreshold) {
      return getComputedStyle(document.body).getPropertyValue('--free-color');
    } else if (usage <= midUsageThreshold) {
      return getComputedStyle(document.body).getPropertyValue('--mid-color');
    } else {
      return getComputedStyle(document.body).getPropertyValue('--max-color');
    }
  }
}

function getDegreeUnit(useFahrenheitUnit: boolean): string {
  return useFahrenheitUnit ? i18n.global.t('degreeF').toString() : i18n.global.t('degreeC').toString();
}

export {
  getUUID,
  rounded,
  getUsageColorClass,
  getDegreeUnit,
  getUsageColor
};
