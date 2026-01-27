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
  static class Pair {
    long x, y;
    Pair(long x, long y) {
      this.x = x;
      this.y = y;
    }
    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (!(o instanceof Pair)) return false;
      Pair p = (Pair) o;
      return x == p.x && y == p.y;
    }
    @Override
    public int hashCode() {
      return Objects.hash(x, y);
    }
  }

  static long gcd(long a, long b) {
    while (b != 0) {
      long t = b;
      b = a % b;
      a = t;
    }
    return Math.abs(a);
  }

  public static void main(String[] args) {
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    int N = fs.nextInt();
    int Q = fs.nextInt();
    long[][] XY = new long[N][2];
    for (int i = 0; i < N; i++) {
      XY[i][0] = fs.nextLong();
      XY[i][1] = fs.nextLong();
    }

    Pair[] A = new Pair[N];
    ArrayList<Pair> B = new ArrayList<>();
    ArrayList<Pair> C = new ArrayList<>();

    for (int i = 0; i < N; i++) {
      long X = XY[i][0], Y = XY[i][1];
      long M = gcd(Math.abs(X), Math.abs(Y));
      long nx = X / M, ny = Y / M;
      A[i] = new Pair(nx, ny);
      if (X == 0) {
        if (Y > 0) B.add(new Pair(nx, ny));
        else C.add(new Pair(nx, ny));
      } else if (X > 0) {
        B.add(new Pair(nx, ny));
      } else {
        C.add(new Pair(nx, ny));
      }
    }

    Comparator<Pair> comp = (r1, r2) -> {
      long X1 = r1.x, Y1 = r1.y, X2 = r2.x, Y2 = r2.y;
      return Long.compare(-(X2 * Y1 - Y2 * X1), 0);
    };

    B.sort(comp);
    C.sort(comp);

    ArrayList<Pair> ANS = new ArrayList<>();
    ANS.addAll(B);
    ANS.addAll(C);

    HashMap<Pair, Integer> D = new HashMap<>();
    HashMap<Pair, Integer> E = new HashMap<>();
    for (int i = 0; i < N; i++) {
      Pair p = ANS.get(i);
      D.putIfAbsent(p, i);
      E.put(p, i + 1);
    }

    for (int q = 0; q < Q; q++) {
      int A_IDX = fs.nextInt() - 1;
      int B_IDX = fs.nextInt() - 1;
      int IDX0 = D.get(A[A_IDX]);
      int IDX1 = E.get(A[B_IDX]);
      int RESULT = (IDX1 - IDX0) % N;
      if (RESULT == 0) RESULT = N;
      out.println(RESULT);
    }
    out.flush();
  }
}