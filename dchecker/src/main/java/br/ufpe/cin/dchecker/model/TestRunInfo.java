package br.ufpe.cin.dchecker.model;

/**
 * Information about a test execution.
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class TestRunInfo implements CheckableInfo {

	public static final String COLUMN_SEP = ";";

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
	private Verdict result;

	/**
	 * Host VM where this test was executed
	 */
	private String host;

	/**
	 * Thread where this test was executed
	 */
	private String thread;

	/**
	 * This test name;
	 */
	private String name;

	@Override
	public String hostVm() {
		return host;
	}

	@Override
	public String name() {
		return this.name;
	}

	@Override
	public long startTime() {
		return this.start;
	}

	@Override
	public long finishedTime() {
		return this.end;
	}

	@Override
	public boolean hasFailed() {
		return this.result.equals(Verdict.FAIL);
	}

	@Override
	public boolean hasOverlap(CheckableInfo other) {
		return (other.finishedTime() >= this.start) && (other.startTime() <= this.end);
	}

	@Override
	public boolean isSameHostVM(CheckableInfo other) {
		return this.hostVm().equals(other.hostVm());
	}

	/**
	 * @param start
	 *            the start to set
	 */
	public void setStart(long start) {
		this.start = start;
	}

	/**
	 * @param end
	 *            the end to set
	 */
	public void setEnd(long end) {
		this.end = end;
	}

	/**
	 * @param result
	 *            the result to set
	 */
	public void setResult(Verdict result) {
		if (this.result == null)
			this.result = result;
	}

	/**
	 * @param host
	 *            the host to set
	 */
	public void setHost(String host) {
		if (this.host == null)
			this.host = host;
	}

	/**
	 * @param thread
	 *            the thread to set
	 */
	public void setThread(String thread) {
		if (this.thread == null)
			this.thread = thread;
	}

	/**
	 * @param name
	 *            the name to set
	 */
	public void setName(String name) {
		if (this.name == null)
			this.name = name;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(name).append(COLUMN_SEP);
		sb.append(start).append(COLUMN_SEP);
		sb.append(end).append(COLUMN_SEP);
		sb.append(thread).append(COLUMN_SEP);
		sb.append(host).append(COLUMN_SEP);
		sb.append(result.name());
		return sb.toString();
	}

	public static TestRunInfo parseRunningInfo(String string) {
		String[] entryLineFields = string.split(COLUMN_SEP);

		TestRunInfo info = new TestRunInfo();
		info.setName(entryLineFields[0]);
		info.setStart(Long.parseLong(entryLineFields[1]));
		info.setEnd(Long.parseLong(entryLineFields[2]));
		info.setThread(entryLineFields[3]);
		info.setHost(entryLineFields[4]);
		info.setResult(Verdict.valueOf(entryLineFields[5]));

		return info;
	}
}
