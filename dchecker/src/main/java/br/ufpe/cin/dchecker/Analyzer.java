package br.ufpe.cin.dchecker;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;

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
		Map<String, Integer> vms = new HashMap<>();
		int dependencyCounter = 0;
		for (Entry<String, RunningInfo> entry : all.entrySet()) {
			dependencyCounter += checkDependencies(entry, all);
			vms.put(entry.getValue().host,
					!vms.containsKey(entry.getValue().host) ? 1 : vms.get(entry.getValue().host) + 1);
		}

		System.out.println("-------- Running Information --------");
		int vmCounter = 0;
		int total = 0;
		for (Entry<String, Integer> entry : vms.entrySet()) {
			total += entry.getValue();
			System.out.println(String.format(" %2d) %-47s %d tests", ++vmCounter, entry.getKey(), entry.getValue()));
		}
		System.out.println("-------- Statistics --------");
		System.out.println(String.format(" %12s: %d", "Total Tests", total));
		System.out.println(String.format(" %12s: %d", "Dependencies", dependencyCounter));
		System.out.println(String.format(" %12s: %d", "VM Counter", vms.size()));

	}

	public static int checkDependencies(Entry<String, RunningInfo> entry, Map<String, RunningInfo> allTests) {
		int dependencyCounter = 0;

		// If result is different from FAIL, this entry has no dependency
		if (!entry.getValue().result.equals(Verdict.FAIL)) {
			return dependencyCounter;
		}
		for (Entry<String, RunningInfo> other : allTests.entrySet()) {
			if (!other.getKey().equals(entry.getKey())) {
				RunningInfo entryInfo = entry.getValue();
				RunningInfo otherInfo = other.getValue();

				// Heuristic for test dependency: overlap on the same host VM
				if (hasOverlap(entryInfo, otherInfo) && isSameHostVM(entryInfo, otherInfo)) {
					System.out.println(entry.getKey() + " ==> " + other.getKey());
					System.out.println(" 1) " + entryInfo.toString());
					System.out.println(" 2) " + otherInfo.toString());
					dependencyCounter++;
				}
			}
		}
		return dependencyCounter;
	}

	private static boolean hasOverlap(RunningInfo entry, RunningInfo other) {
		return (other.end >= entry.start) && (other.start <= entry.end);
	}

	private static boolean isSameHostVM(RunningInfo entry, RunningInfo other) {
		return (other.host.equals(entry.host));
	}
}
