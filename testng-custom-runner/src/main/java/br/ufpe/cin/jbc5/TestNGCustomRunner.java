package br.ufpe.cin.jbc5;

import java.io.IOException;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.testng.ITestResult;
import org.testng.TestListenerAdapter;

import br.ufpe.cin.jbc5.RunningInfo.Verdict;

/**
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class TestNGCustomRunner extends TestListenerAdapter {

	private final static Logger LOGGER = Logger.getLogger(TestNGCustomRunner.class.getName());
	static {
		LOGGER.setLevel(Level.INFO);
	}

	@Override
	public void onTestFailure(ITestResult tr) {
		StringBuffer sb = new StringBuffer();

		sb.append(tr.getTestClass().getName()).append(".").append(tr.getName()).append(",");
		sb.append(tr.getStartMillis()).append(",");
		sb.append(tr.getEndMillis()).append(",");
		sb.append(Verdict.FAIL);

		LOGGER.info(sb.toString());

		super.onTestFailure(tr);
	}

	@Override
	public void onTestSuccess(ITestResult tr) {
		StringBuffer sb = new StringBuffer();

		sb.append(tr.getTestClass().getName()).append(".").append(tr.getName()).append(",");
		sb.append(tr.getStartMillis()).append(",");
		sb.append(tr.getEndMillis()).append(",");
		sb.append(Verdict.PASS);

		LOGGER.info(sb.toString());

		super.onTestSuccess(tr);
	}

}
