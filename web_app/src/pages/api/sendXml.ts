import { NextApiRequest, NextApiResponse } from "next";
import axios from "axios";
import getRawBody from "raw-body";

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
): Promise<void> {
  if (req.method !== "POST") {
    res.setHeader("Allow", ["POST"]);
    res.status(405).end("Method Not Allowed");
    return;
  }

  try {
    const xmlBuffer = await getRawBody(req);
    const xmlString = xmlBuffer.toString("utf-8");

    // 🔐 Basic Auth credentials for pdf-gen-service
    const username = `${process.env.PDF_GEN_USER}`;
    const password = `${process.env.PDF_GEN_PASS}`;
    const basicAuth = Buffer.from(`${username}:${password}`).toString("base64");

    const remoteRes = await axios.post(
      `${process.env.PDF_GEN_BASE_URL}` + "/renderpdf",
      xmlString,
      {
        headers: {
          "Content-Type": "text/html",
          Accept: "text/html",
          Authorization: `Basic ${basicAuth}`,
        },
        responseType: "arraybuffer",
      }
    );

    res.setHeader("Content-Type", "application/pdf");
    res.setHeader("Content-Disposition", "attachment; filename=response.pdf");
    res.status(200).send(Buffer.from(remoteRes.data));
  } catch (error) {
    console.error("Error posting XML or fetching PDF:", error);
    res.status(500).json({ error: "Failed to fetch PDF" });
  }
}
