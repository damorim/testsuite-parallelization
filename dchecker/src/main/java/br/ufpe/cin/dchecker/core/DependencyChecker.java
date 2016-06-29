package br.ufpe.cin.dchecker.core;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import br.ufpe.cin.dchecker.info.RunningInfo;
import br.ufpe.cin.dchecker.info.Verdict;

public class DependencyChecker {

	public static int checkDependencies(Entry<String, RunningInfo> entry, Map<String, RunningInfo> allTests) {
		int dependencyCounter = 0;

		// If result is different from FAIL, this entry has no dependency
		if (!entry.getValue().getResult().equals(Verdict.FAIL)) {
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
		return (other.getEnd() >= entry.getStart()) && (other.getStart() <= entry.getEnd());
	}

	private static boolean isSameHostVM(RunningInfo entry, RunningInfo other) {
		return (other.getHost().equals(entry.getHost()));
	}

	public static void run(Map<String, RunningInfo> all) {
		// Check dependencies
		Map<String, Integer> vms = new HashMap<>();
		int dependencyCounter = 0;
		for (Entry<String, RunningInfo> entry : all.entrySet()) {
			dependencyCounter += checkDependencies(entry, all);
			vms.put(entry.getValue().getHost(),
					!vms.containsKey(entry.getValue().getHost()) ? 1 : vms.get(entry.getValue().getHost()) + 1);
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
}
