package br.ufpe.cin.dchecker.model;

/**
 * Test verdicts.
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public enum Verdict {
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