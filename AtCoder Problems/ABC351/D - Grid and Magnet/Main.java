import java.io.*;
import java.util.*;

class FastScanner {
  private final InputStream in = System.in;
  private final byte[] buffer = new byte[1024];
  private int ptr = 0;
  private int buflen = 0;

  private boolean hasNextByte() {
    if (ptr < buflen) {
      return true;
    } else {
      ptr = 0;
      try {
        buflen = in.read(buffer);
      } catch (IOException e) {
        e.printStackTrace();
      }
      if (buflen <= 0) {
        return false;
      }
    }
    return true;
  }

  private int readByte() {
    if (hasNextByte())
      return buffer[ptr++];
    else
      return -1;
  }

  private static boolean isPrintableChar(int c) {
    return 33 <= c && c <= 126;
  }

  public boolean hasNext() {
    while (hasNextByte() && !isPrintableChar(buffer[ptr]))
      ptr++;
    return hasNextByte();
  }

  public String next() {
    if (!hasNext())
      throw new NoSuchElementException();
    StringBuilder sb = new StringBuilder();
    int b = readByte();
    while (isPrintableChar(b)) {
      sb.appendCodePoint(b);
      b = readByte();
    }
    return sb.toString();
  }

  public long nextLong() {
    if (!hasNext())
      throw new NoSuchElementException();
    long n = 0;
    boolean minus = false;
    int b = readByte();
    if (b == '-') {
      minus = true;
      b = readByte();
    }
    if (b < '0' || '9' < b) {
      throw new NumberFormatException();
    }
    while (true) {
      if ('0' <= b && b <= '9') {
        n *= 10;
        n += b - '0';
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
    if (nl < Integer.MIN_VALUE || nl > Integer.MAX_VALUE)
      throw new NumberFormatException();
    return (int) nl;
  }

  public double nextDouble() {
    return Double.parseDouble(next());
  }
}

public class Main {
  static int h, w;
  static char[][] grid;
  static boolean[] good;
  static int[] used;
  static int[] stack;
  static int[] dx = {0, 0, 1, -1};
  static int[] dy = {1, -1, 0, 0};

  static int dfsIter(int start) {
    int top = 0;
    stack[top++] = start;
    used[start] = start;
    int cnt = 0;

    while (top > 0) {
      int v = stack[--top];
      cnt++;
      if (!good[v]) continue;

      int x = v / w;
      int y = v % w;
      for (int k = 0; k < 4; k++) {
        int nx = x + dx[k];
        int ny = y + dy[k];
        if (nx < 0 || nx >= h || ny < 0 || ny >= w) continue;
        if (grid[nx][ny] == '#') continue;
        int to = nx * w + ny;
        if (used[to] == start) continue;
        used[to] = start;
        stack[top++] = to;
      }
    }
    return cnt;
  }

  public static void main(String[] args) throws Exception {
    FastScanner fs = new FastScanner();
    h = fs.nextInt();
    w = fs.nextInt();
    grid = new char[h][w];
    for (int i = 0; i < h; i++) grid[i] = fs.next().toCharArray();

    int n = h * w;
    good = new boolean[n];
    used = new int[n];
    Arrays.fill(used, -1);
    stack = new int[n];

    for (int i = 0; i < h; i++) {
      for (int j = 0; j < w; j++) {
        if (grid[i][j] == '#') {
          good[i * w + j] = false;
          continue;
        }
        boolean can = true;
        for (int k = 0; k < 4; k++) {
          int ni = i + dx[k];
          int nj = j + dy[k];
          if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
          if (grid[ni][nj] == '#') {
            can = false;
            break;
          }
        }
        good[i * w + j] = can;
      }
    }

    int ans = 0;
    for (int i = 0; i < h; i++) {
      for (int j = 0; j < w; j++) {
        int v = i * w + j;
        if (grid[i][j] == '.' && used[v] < 0) {
          int cnt = dfsIter(v);
          if (cnt > ans) ans = cnt;
        }
      }
    }
    System.out.println(ans);
  }
}