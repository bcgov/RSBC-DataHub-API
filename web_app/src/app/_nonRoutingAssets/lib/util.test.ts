import { getInitials, validateRequired } from './util';

describe('getInitials', () => {
    it('should return the initials of a name', () => {
        expect(getInitials('John Doe')).toBe('JD');
    });

    it('should return empty string if name is null', () => {
        expect(getInitials(null)).toBe('');
    });

    it('should return empty string if name is undefined', () => {
        expect(getInitials(undefined)).toBe('');
    });

    it('should ignore special characters and spaces', () => {
        expect(getInitials('John-Doe Smith')).toBe('JDS');
    });
});


describe('validateRequired', () => {
    it ('should return false if value is null', () => {
        expect(validateRequired(null) == false);
    });

    it ('should return false if value is undefined', () => {
        expect(validateRequired(undefined) == false);
    });

    it ('should return false if value is empty string', () => {
        expect(validateRequired('') == false);
    });

    it ('should return false if value is empty string v2', () => {
        expect(validateRequired(' ') == false);
    });

    it ('should return true if value is non blank', () => {
        expect(validateRequired('some string') == true);
    });    
});