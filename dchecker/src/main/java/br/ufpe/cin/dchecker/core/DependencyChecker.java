package br.ufpe.cin.dchecker.core;

import java.util.HashSet;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import br.ufpe.cin.dchecker.model.DependencyGroup;
import br.ufpe.cin.dchecker.model.RunningInfo;
import br.ufpe.cin.dchecker.model.Verdict;

public class DependencyChecker {

	public static Set<DependencyGroup> dependenciesFrom(Map<String, RunningInfo> all) {
		HashSet<DependencyGroup> allDependencies = new HashSet<>();
		for (Entry<String, RunningInfo> entry : all.entrySet()) {
			DependencyGroup dependencyGroup = dependencyGroupFrom(entry, all);
			if (dependencyGroup != null) {
				allDependencies.add(dependencyGroup);
			}
		}
		return allDependencies;
	}

	private static DependencyGroup dependencyGroupFrom(Entry<String, RunningInfo> entry, Map<String, RunningInfo> all) {
		// If result is different from FAIL, this entry has no dependency.
		if (!hasFailed(entry)) {
			return null;
		}
		DependencyGroup dependencyGroup = new DependencyGroup(entry);
		for (Entry<String, RunningInfo> other : all.entrySet()) {
			if (!other.getKey().equals(entry.getKey())) {
				RunningInfo failingEntryInfo = entry.getValue();
				RunningInfo otherInfo = other.getValue();

				// Heuristic for test dependency: overlap on the same host VM
				if (hasOverlap(failingEntryInfo, otherInfo) && isSameHostVM(failingEntryInfo, otherInfo)) {
					dependencyGroup.put(other);
				}
			}
		}
		return dependencyGroup;
	}

	private static boolean hasFailed(Entry<String, RunningInfo> failingEntry) {
		return failingEntry.getValue().getResult().equals(Verdict.FAIL);
	}

	private static boolean hasOverlap(RunningInfo entry, RunningInfo other) {
		return (other.getEnd() >= entry.getStart()) && (other.getStart() <= entry.getEnd());
	}

	private static boolean isSameHostVM(RunningInfo entry, RunningInfo other) {
		return (other.getHost().equals(entry.getHost()));
	}

}
