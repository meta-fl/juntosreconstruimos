import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const dataPath = path.join(process.cwd(), 'data', 'matriz.json');

export async function GET() {
  try {
    const fileContents = fs.readFileSync(dataPath, 'utf8');
    const data = JSON.parse(fileContents);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json([]);
  }
}

export async function POST(request) {
  const body = await request.json();
  const fileContents = fs.readFileSync(dataPath, 'utf8');
  const data = JSON.parse(fileContents);
  
  const newItem = {
    id: data.length > 0 ? Math.max(...data.map(d => d.id)) + 1 : 1,
    ...body
  };
  
  data.push(newItem);
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2), 'utf8');
  
  return NextResponse.json(data);
}
