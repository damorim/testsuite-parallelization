package br.ufpe.cin.jbc5;

import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.ConcurrentHashMap;

import org.testng.IExecutionListener;
import org.testng.ITestResult;
import org.testng.TestListenerAdapter;

import br.ufpe.cin.jbc5.RunningInfo.Status;

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
		i.result = Status.FAIL;

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
		i.result = Status.PASS;

		this.allTests.put(sb.toString(), i);
		super.onTestSuccess(tr);
	}

	@Override
	public void onExecutionFinish() {
		System.out.println("Test, Start, Finished, Result");
		for (Map.Entry<String, RunningInfo> entry : allTests.entrySet()) {
			System.out.println(entry.getKey() + ", " + entry.getValue());
		}
		for (Map.Entry<String, RunningInfo> entry : allTests.entrySet()) {
			checkDependencies(entry);
		}
	}

	private void checkDependencies(Entry<String, RunningInfo> entry) {
		// If result is different from FAIL, this entry has no dependency
		if (!entry.getValue().result.equals(Status.FAIL)) {
			return;
		}
		for (Map.Entry<String, RunningInfo> other : allTests.entrySet()) {
			if (!other.getKey().equals(entry.getKey())) {
				RunningInfo entryInfo = entry.getValue();
				RunningInfo otherInfo = other.getValue();
				if (hasOverlap(entryInfo, otherInfo)) {
					System.out.println(entry.getKey() + " ==> " + other.getKey());
				}
			}
		}

	}

	private boolean hasOverlap(RunningInfo entry, RunningInfo other) {
		return !((other.end < entry.start) || (other.start > entry.end));
	}

}
