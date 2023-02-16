export default {
  checkDigit(prohibition_number) {
    // calculate the check digit of a six-digit prohibition number
    const n = Array.from(prohibition_number.toString()).map(Number);
    const number_sum = (
      n[0] + this.timesTwo(n[1]) +
      n[2] + this.timesTwo(n[3]) +
      n[4] + this.timesTwo(n[5])
    );
    return number_sum % 10;
  },
  timesTwo(number) {
    // if number * 2 is greater than 9, return 1 otherwise return the number * 2
    return parseInt(((number * 2).toString()).split()[0]);
  }
}