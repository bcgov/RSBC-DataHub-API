// // src/types/jspdf.d.ts
// import { jsPDF } from 'jspdf';

// declare module 'jspdf' {
//     interface jsPDF {
//         internal: {
//             getNumberOfPages: () => number;
//             pageSize: {
//                 width: number;
//                 height: number;
//             };
//             [key: string]: any; // Add this line to allow other properties
//         };
//     }
// }