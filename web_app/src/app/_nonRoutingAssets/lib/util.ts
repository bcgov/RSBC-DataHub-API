export function getInitials(name: string | null | undefined) {
    if (!name)
        return '';

    return name?.replace(/[^a-zA-Z- ]/g, "")?.match(/\b\w/g)?.join("").toUpperCase();
}

export const validateRequired = (value: string | null | undefined) => !!value?.length;


export const prohibitionNumberRegex = /^(00|21|30|40)-\d{6}$/;