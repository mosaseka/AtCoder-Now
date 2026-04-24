import java.io.*
import java.util.*

fun main() {
  val fs = FastScanner()
  val n = fs.nextInt()
  val m = fs.nextInt()

  val graph = Array(n + 1) { mutableListOf<Int>() }
  repeat(m) {
    val a = fs.nextInt()
    val b = fs.nextInt()
    graph[a].add(b)
  }

  val visited = BooleanArray(n + 1)
  val stack = ArrayDeque<Int>()
  stack.addLast(1)
  visited[1] = true
  var answer = 1

  while (stack.isNotEmpty()) {
    val v = stack.removeLast()
    for (nv in graph[v]) {
      if (!visited[nv]) {
        visited[nv] = true
        stack.addLast(nv)
        answer++
      }
    }
  }

  println(answer)
}

class FastScanner {
  private val input = BufferedInputStream(System.`in`)
  private val buffer = ByteArray(1024)
  private var ptr = 0
  private var buflen = 0

  private fun hasNextByte(): Boolean {
    if (ptr < buflen) {
      return true
    }

    ptr = 0
    buflen = input.read(buffer)
    return buflen > 0
  }

  private fun readByte(): Int {
    return if (hasNextByte()) {
      buffer[ptr++].toInt()
    } else {
      -1
    }
  }

  private fun isPrintableChar(c: Int): Boolean {
    return c in 33..126
  }

  fun hasNext(): Boolean {
    while (hasNextByte() && !isPrintableChar(buffer[ptr].toInt())) {
      ptr++
    }
    return hasNextByte()
  }

  fun next(): String {
    if (!hasNext()) {
      throw NoSuchElementException()
    }

    val sb = StringBuilder()
    var b = readByte()
    while (isPrintableChar(b)) {
      sb.append(b.toChar())
      b = readByte()
    }
    return sb.toString()
  }

  fun nextLong(): Long {
    if (!hasNext()) {
      throw NoSuchElementException()
    }

    var n = 0L
    var minus = false
    var b = readByte()
    if (b == '-'.code) {
      minus = true
      b = readByte()
    }
    if (b < '0'.code || '9'.code < b) {
      throw NumberFormatException()
    }

    while (true) {
      if ('0'.code <= b && b <= '9'.code) {
        n *= 10
        n += (b - '0'.code).toLong()
      } else if (b == -1 || !isPrintableChar(b)) {
        return if (minus) -n else n
      } else {
        throw NumberFormatException()
      }
      b = readByte()
    }
  }

  fun nextInt(): Int {
    val nl = nextLong()
    if (nl < Int.MIN_VALUE || Int.MAX_VALUE < nl) {
      throw NumberFormatException()
    }
    return nl.toInt()
  }

  fun nextDouble(): Double {
    return next().toDouble()
  }
}
