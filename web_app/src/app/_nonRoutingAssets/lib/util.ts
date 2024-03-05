export const validateRequired = (value: string | null | undefined) => !!value?.length;

const prohibitionNumberRegex = /^(00|21|30|40)-\d{6}$/;
export const isProhibitionNumberValid = 
    (value: string) => prohibitionNumberRegex.exec(value);
