import java.io.*;
import java.util.*;

class FastScanner {
  private final InputStream in = System.in;
  private final byte[] buffer = new byte[1024];
  private int ptr = 0;
  private int buflen = 0;

  private boolean hasNextByte() {
    if (ptr < buflen) return true;
    ptr = 0;
    try { buflen = in.read(buffer); }
    catch (IOException e) { e.printStackTrace(); }
    return buflen > 0;
  }

  private int readByte() {
    return hasNextByte() ? buffer[ptr++] : -1;
  }

  private static boolean isPrintableChar(int c) {
    return 33 <= c && c <= 126;
  }

  public boolean hasNext() {
    while (hasNextByte() && !isPrintableChar(buffer[ptr])) ptr++;
    return hasNextByte();
  }

  public String next() {
    if (!hasNext()) throw new NoSuchElementException();
    StringBuilder sb = new StringBuilder();
    int b = readByte();
    while (isPrintableChar(b)) {
      sb.appendCodePoint(b);
      b = readByte();
    }
    return sb.toString();
  }

  public long nextLong() {
    if (!hasNext()) throw new NoSuchElementException();
    long n = 0;
    boolean minus = false;
    int b = readByte();
    if (b == '-') { minus = true; b = readByte(); }
    if (b < '0' || '9' < b) throw new NumberFormatException();
    while (true) {
      if ('0' <= b && b <= '9') {
        n = n * 10 + (b - '0');
      } else if (b == -1 || !isPrintableChar(b)) {
        return minus ? -n : n;
      } else {
        throw new NumberFormatException();
      }
      b = readByte();
    }
  }

  public int nextInt() {
    long nl = nextLong();
    if (nl < Integer.MIN_VALUE || nl > Integer.MAX_VALUE) throw new NumberFormatException();
    return (int) nl;
  }
}

public class Main {
  static int l;
  static int s, t;
  static ArrayList<Edge>[] g;
  static boolean[] flag;

  static class Edge {
    int to, cost;
    Edge(int to, int cost) { this.to = to; this.cost = cost; }
  }

  static void dfs(int k, int d, int tot) {
    if (d == l) {
      if (s <= tot && tot <= t) flag[k] = true;
      return;
    }
    if (d < l) {
      for (Edge ed : g[k]) dfs(ed.to, d + 1, tot + ed.cost);
    }
  }

  public static void main(String[] args) {
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    int N = fs.nextInt();
    int M = fs.nextInt();
    l = fs.nextInt();
    s = fs.nextInt();
    t = fs.nextInt();

    g = new ArrayList[N];
    for (int i = 0; i < N; i++) g[i] = new ArrayList<>();

    for (int i = 0; i < M; i++) {
      int U = fs.nextInt();
      int V = fs.nextInt();
      int C = fs.nextInt();
      g[U - 1].add(new Edge(V - 1, C));
    }

    flag = new boolean[N];
    dfs(0, 0, 0);

    StringBuilder sb = new StringBuilder();
    boolean first = true;
    for (int i = 0; i < N; i++) {
      if (flag[i]) {
        if (!first) sb.append(' ');
        sb.append(i + 1);
        first = false;
      }
    }
    out.println(sb.toString());
    out.flush();
  }
}
