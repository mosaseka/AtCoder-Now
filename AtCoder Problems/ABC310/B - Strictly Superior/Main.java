import java.io.*;
import java.util.*;

public class Main{
  public static void main(String[] args){
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    int N = fs.nextInt();
    int M = fs.nextInt();

    int[] p = new int[N];
    int[] c = new int[N];
    List<int[]> features = new ArrayList<>(N);
    List<Set<Integer>> featureSets = new ArrayList<>(N);

    for (int i = 0; i < N; i++){
      p[i] = fs.nextInt();
      c[i] = fs.nextInt();
      int[] f = new int[c[i]];
      Set<Integer> set = new HashSet<>();
      for (int k = 0; k < c[i]; k++){
        f[k] = fs.nextInt();
        set.add(f[k]);
      }
      features.add(f);
      featureSets.add(set);
    }

    boolean ok = false;
    for (int i = 0; i < N && !ok; i++){
      for (int j = 0; j < N && !ok; j++){
        if (i == j) continue;
        if (p[i] >= p[j]){
          boolean alpha = true;
          Set<Integer> setJ = featureSets.get(j);
          for (int v : features.get(i)){
            if (!setJ.contains(v)){
              alpha = false;
              break;
            }
          }
          boolean beta = (p[i] > p[j]) || (features.get(j).length > features.get(i).length);
          if (alpha && beta){
            ok = true;
          }
        }
      }
    }
    out.println(ok ? "Yes" : "No");
    out.flush();
  }
}


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