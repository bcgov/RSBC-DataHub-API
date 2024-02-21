export function getInitials(name: string | null | undefined) {
    if (!name)
        return '';

    return name?.replace(/[^a-zA-Z- ]/g, "")?.match(/\b\w/g)?.join("").toUpperCase();
}

export const validateRequired = (value: string | null | undefined) => !!value?.length;