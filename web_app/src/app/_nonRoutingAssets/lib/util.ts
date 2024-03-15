export const validateRequired = (value: string | null | undefined) => !!value?.length;

const prohibitionNumberRegex = /^(00|21|30|40)-\d{6}$/;
export const isProhibitionNumberValid =
    (value: string) => prohibitionNumberRegex.exec(value);

export const file2Base64 = (file: File): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result?.toString() || '');
        reader.onerror = error => reject(error);
    })
}