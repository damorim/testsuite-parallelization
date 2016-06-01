package br.ufpe.cin.jbc5;

import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.ConcurrentHashMap;

import org.testng.ITestContext;
import org.testng.ITestResult;
import org.testng.TestListenerAdapter;

public class TestNGCustomRunner extends TestListenerAdapter {

	enum Status {
		TORUN, PASS, FAIL;
	}

	private class Info {

		long start;
		long end;
		Status result = Status.TORUN;

		@Override
		public String toString() {
			StringBuilder sb = new StringBuilder();
			sb.append(start).append(", ");
			sb.append(end).append(", ");
			sb.append(result.name());
			return sb.toString();
		}
	}

	private Map<String, Info> allTests;

	@Override
	public void onStart(ITestContext testContext) {
		this.allTests = new ConcurrentHashMap<>();
		super.onStart(testContext);
	}

	@Override
	public void onTestFailure(ITestResult tr) {
		StringBuffer sb = new StringBuffer();
		sb.append(tr.getTestClass().getName()).append(".").append(tr.getName());

		Info i = new Info();
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

		Info i = new Info();
		i.start = tr.getStartMillis();
		i.end = tr.getEndMillis();
		i.result = Status.PASS;

		this.allTests.put(sb.toString(), i);
		super.onTestSuccess(tr);
	}

	@Override
	public void onFinish(ITestContext testContext) {
		System.out.println("===== Tests Summary =====");
		for (Map.Entry<String, Info> entry : allTests.entrySet()) {
			System.out.println(entry.getKey() + ":\t" + entry.getValue());
		}
		System.out.println("===== Dependencies =====");
		for (Map.Entry<String, Info> entry : allTests.entrySet()) {
			checkDependencies(entry);
		}
		super.onFinish(testContext);
	}

	private void checkDependencies(Entry<String, Info> entry) {
		// If result is different from FAIL, this entry has no dependency
		if (!entry.getValue().result.equals(Status.FAIL)) {
			return;
		}
		for (Map.Entry<String, Info> other : allTests.entrySet()) {
			if (!other.getKey().equals(entry.getKey())) {
				Info entryInfo = entry.getValue();
				Info otherInfo = other.getValue();
				if (hasOverlap(entryInfo, otherInfo)) {
					System.out.println(entry.getKey() + " ==> " + other.getKey());
				}
			}
		}
	}

	private boolean hasOverlap(Info entry, Info other) {
		return !((other.end < entry.start) || (other.start > entry.end));
	}

}
