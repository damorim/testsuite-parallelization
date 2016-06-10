package br.ufpe.cin.dchecker;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;

import br.ufpe.cin.dchecker.RunningInfo;
import br.ufpe.cin.dchecker.RunningInfo.Verdict;

/**
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class Analyzer {

	public static void main(String[] args) throws FileNotFoundException {
		String name = args[0];
		Scanner sc = new Scanner(new BufferedInputStream(new FileInputStream(name)));

		// Parse and load all entries in memory
		Map<String, RunningInfo> all = new HashMap<>();
		while (sc.hasNext()) {
			String[] entryLineFields = sc.nextLine().split(",");
			String key = entryLineFields[0];
			RunningInfo info = new RunningInfo();
			info.start = Long.parseLong(entryLineFields[1]);
			info.end = Long.parseLong(entryLineFields[2]);
			info.host = entryLineFields[3];
			info.result = Verdict.valueOf(entryLineFields[4]);
			all.put(key, info);
		}
		sc.close();

		// Check dependencies
		for (Map.Entry<String, RunningInfo> entry : all.entrySet()) {
			checkDependencies(entry, all);
		}
	}

	public static void checkDependencies(Entry<String, RunningInfo> entry, Map<String, RunningInfo> allTests) {
		// If result is different from FAIL, this entry has no dependency
		if (!entry.getValue().result.equals(Verdict.FAIL)) {
			return;
		}
		for (Map.Entry<String, RunningInfo> other : allTests.entrySet()) {
			if (!other.getKey().equals(entry.getKey())) {
				RunningInfo entryInfo = entry.getValue();
				RunningInfo otherInfo = other.getValue();

				// Heuristic for test dependency: overlap on the same host VM
				if (hasOverlap(entryInfo, otherInfo) && isSameHostVM(entryInfo, otherInfo)) {
					System.out.println(entry.getKey() + " ==> " + other.getKey());
				}
			}
		}

	}

	private static boolean hasOverlap(RunningInfo entry, RunningInfo other) {
		return !((other.end < entry.start) || (other.start > entry.end));
	}

	private static boolean isSameHostVM(RunningInfo entry, RunningInfo other) {
		return (other.host.equals(entry.host));
	}
}
