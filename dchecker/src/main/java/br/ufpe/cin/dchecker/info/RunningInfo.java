package br.ufpe.cin.dchecker.info;

/**
 * Information about a test execution.
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class RunningInfo {

	/**
	 * When the test has started (in milliseconds).
	 */
	private long start;
	/**
	 * When the test has finished (in milliseconds).
	 */
	private long end;

	/**
	 * Verdict for this test execution.
	 */
	private Verdict result = Verdict.UNKNOWN;

	/**
	 * Host VM where this test was executed
	 */
	private String host;
	/**
	 * Thread where this test was executed
	 */
	private String thread;

	/**
	 * @return the start
	 */
	public long getStart() {
		return start;
	}

	/**
	 * @param start
	 *            the start to set
	 */
	public void setStart(long start) {
		this.start = start;
	}

	/**
	 * @return the end
	 */
	public long getEnd() {
		return end;
	}

	/**
	 * @param end
	 *            the end to set
	 */
	public void setEnd(long end) {
		this.end = end;
	}

	/**
	 * @return the result
	 */
	public Verdict getResult() {
		return result;
	}

	/**
	 * @param result
	 *            the result to set
	 */
	public void setResult(Verdict result) {
		this.result = result;
	}

	/**
	 * @return the host
	 */
	public String getHost() {
		return host;
	}

	/**
	 * @param host
	 *            the host to set
	 */
	public void setHost(String host) {
		this.host = host;
	}

	/**
	 * @return the thread
	 */
	public String getThread() {
		return thread;
	}

	/**
	 * @param thread
	 *            the thread to set
	 */
	public void setThread(String thread) {
		this.thread = thread;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(start).append(", ");
		sb.append(end).append(", ");
		sb.append(thread).append(", ");
		sb.append(host).append(", ");
		sb.append(result.name());
		return sb.toString();
	}
}
