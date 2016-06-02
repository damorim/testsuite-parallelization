package br.ufpe.cin.jbc5;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
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
		List<String> reportLines = new ArrayList<>();
		reportLines.add("Test, Start, Finished, Result");
		for (Map.Entry<String, RunningInfo> entry : allTests.entrySet()) {
			reportLines.add(entry.getKey() + ", " + entry.getValue());
		}
		Path file = Paths.get("timestamps.csv");
		try {
			Files.write(file, reportLines, Charset.forName("UTF-8"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
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
		List<String> dependencies = new ArrayList<>();
		for (Map.Entry<String, RunningInfo> other : allTests.entrySet()) {
			if (!other.getKey().equals(entry.getKey())) {
				RunningInfo entryInfo = entry.getValue();
				RunningInfo otherInfo = other.getValue();
				if (hasOverlap(entryInfo, otherInfo)) {
					dependencies.add(entry.getKey() + " ==> " + other.getKey());
				}
			}
		}
		Path file = Paths.get("dependencies.txt");
		try {
			Files.write(file, dependencies, Charset.forName("UTF-8"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	private boolean hasOverlap(RunningInfo entry, RunningInfo other) {
		return !((other.end < entry.start) || (other.start > entry.end));
	}

}
