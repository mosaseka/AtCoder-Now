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

class SegTree {
  private int n, num;
  private long[] tree;
  private final long ide_ele = 0L; // 単位元（加算なら0)

  // 区間和用
  public SegTree(long[] init_val) {
    this.n = init_val.length;
    this.num = 1;
    while (this.num < n) this.num <<= 1;
    this.tree = new long[2 * this.num];
    Arrays.fill(this.tree, ide_ele);
    // 葉にセット
    for (int i = 0; i < n; i++) {
      this.tree[this.num + i] = init_val[i];
    }
    // 構築
    for (int i = this.num - 1; i > 0; i--) {
      this.tree[i] = this.tree[2 * i] + this.tree[2 * i + 1];
    }
  }

  // k番目(0-indexed)をxに更新
  public void update(int k, long x) {
    k += this.num;
    this.tree[k] = x;
    while (k > 1) {
      k >>= 1;
      this.tree[k] = this.tree[2 * k] + this.tree[2 * k + 1];
    }
  }

  // [l, r) の区間和
  public long query(int l, int r) {
    long res = ide_ele;
    l += this.num;
    r += this.num;
    while (l < r) {
      if ((l & 1) == 1) res += this.tree[l++];
      if ((r & 1) == 1) res += this.tree[--r];
      l >>= 1;
      r >>= 1;
    }
    return res;
  }
}

public class Main{
  public static void main(String[] args){
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    long N = fs.nextLong();
    long Q = fs.nextLong();

    long[] A_LIST = new long[(int)N];
    for(int i = 0; i < N; i++){
      A_LIST[i] = fs.nextLong();
    }

    SegTree st = new SegTree(A_LIST);

    for (int i = 0; i < Q; i++){
      int queryType = fs.nextInt();

      switch (queryType){
        case 1:
          int x = fs.nextInt() - 1;

          long temp = A_LIST[x];
          A_LIST[x] = A_LIST[x + 1];
          A_LIST[x + 1] = temp;

          st.update(x, A_LIST[x]);
          st.update(x + 1, A_LIST[x + 1]);
          break;
        case 2:
          int l = fs.nextInt() - 1;
          int r = fs.nextInt() - 1;
          out.println(st.query(l, r+1));
          break;
      }
    }
    out.flush();
  }
}