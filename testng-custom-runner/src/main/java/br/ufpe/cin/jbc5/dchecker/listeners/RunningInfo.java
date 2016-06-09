package br.ufpe.cin.jbc5.dchecker.listeners;

/**
 * Information about a test execution.
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
class RunningInfo {

	/**
	 * Test verdicts.
	 *
	 * @author Jeanderson Candido <http://jeandersonbc.github.io>
	 *
	 */
	enum Verdict {
		/**
		 * Test does not have a verdict yet.
		 */
		UNKNOWN,
		/**
		 * Test has passed.
		 */
		PASS,
		/**
		 * Test has failed.
		 */
		FAIL;
	}

	/**
	 * When the test has started (in milliseconds).
	 */
	long start;
	/**
	 * When the test has finished (in milliseconds).
	 */
	long end;

	/**
	 * Verdict for this test execution.
	 */
	Verdict result = Verdict.UNKNOWN;

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(start).append(", ");
		sb.append(end).append(", ");
		sb.append(result.name());
		return sb.toString();
	}
}