package br.ufpe.cin.jbc5;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.testng.IExecutionListener;
import org.testng.ITestResult;
import org.testng.TestListenerAdapter;

import br.ufpe.cin.jbc5.RunningInfo.Verdict;

/**
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class TestNGCustomRunner extends TestListenerAdapter implements IExecutionListener {

	private Map<String, RunningInfo> allTests;

	@Override
	public void onExecutionStart() {
		this.allTests = new ConcurrentHashMap<>();
	}

	@Override
	public void onTestFailure(ITestResult tr) {
		StringBuffer sb = new StringBuffer();
		sb.append(tr.getTestClass().getName()).append(".").append(tr.getName());

		RunningInfo i = new RunningInfo();
		i.start = tr.getStartMillis();
		i.end = tr.getEndMillis();
		i.result = Verdict.FAIL;

		this.allTests.put(sb.toString(), i);
		super.onTestFailure(tr);
	}

	@Override
	public void onTestSuccess(ITestResult tr) {
		StringBuffer sb = new StringBuffer();
		sb.append(tr.getTestClass().getName()).append(".").append(tr.getName());

		RunningInfo i = new RunningInfo();
		i.start = tr.getStartMillis();
		i.end = tr.getEndMillis();
		i.result = Verdict.PASS;

		this.allTests.put(sb.toString(), i);
		super.onTestSuccess(tr);
	}

	@Override
	public void onExecutionFinish() {
		String prefixPattern = "###";
		for (Map.Entry<String, RunningInfo> entry : allTests.entrySet()) {
			System.out.printf("%s%s, %s\n", prefixPattern, entry.getKey(), entry.getValue());
		}
	}

}
