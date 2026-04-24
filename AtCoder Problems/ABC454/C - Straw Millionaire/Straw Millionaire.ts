import * as fs from "fs";

const input = fs.readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let idx = 0;

const N = input[idx++];
const M = input[idx++];

const graph: number[][] = Array.from({ length: N + 1 }, () => []);

for (let i = 0; i < M; i++) {
  const a = input[idx++];
  const b = input[idx++];
  graph[a].push(b);
}

const visited: boolean[] = Array(N + 1).fill(false);
const stack: number[] = [1];
visited[1] = true;
let answer = 1;

while (stack.length > 0) {
  const v = stack.pop()!;
  for (const nv of graph[v]) {
    if (!visited[nv]) {
      visited[nv] = true;
      stack.push(nv);
      answer++;
    }
  }
}

console.log(answer);