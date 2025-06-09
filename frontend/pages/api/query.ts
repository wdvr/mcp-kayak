import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.status(405).end();
    return;
  }

  const query = req.body.query as string;
  exec(`claude -p "${query}"`, { maxBuffer: 1024 * 1000 }, (err, stdout, stderr) => {
    if (err) {
      res.status(500).json({ error: stderr || err.message });
      return;
    }
    try {
      const data = JSON.parse(stdout);
      res.status(200).json(data);
    } catch {
      res.status(200).json({ output: stdout });
    }
  });
}
