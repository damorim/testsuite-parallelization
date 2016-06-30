package br.ufpe.cin.dchecker.core;

import java.util.HashSet;
import java.util.Set;

import br.ufpe.cin.dchecker.model.CheckableInfo;
import br.ufpe.cin.dchecker.model.DependencyGroup;

public class DependencyAnalyzer {

	static class Options {
		boolean showStatistics = true;
		boolean showRunningInformation = true;
		boolean showDependencyModel = true;
	}

	public static Set<DependencyGroup> check(Set<CheckableInfo> entries) {
		return check(entries, new Options());
	}

	public static Set<DependencyGroup> check(Set<CheckableInfo> entries, Options options) {
		Set<DependencyGroup> allDependencies = dependenciesFrom(entries);
		if (options.showDependencyModel) {
			showDependencyModel(allDependencies);
		}
		if (options.showStatistics) {
			showStatisticsFrom(allDependencies);
		}
		if (options.showRunningInformation) {
			showRunningInformationFrom(entries);
		}
		return allDependencies;
	}

	private static Set<DependencyGroup> dependenciesFrom(Set<CheckableInfo> all) {
		Set<DependencyGroup> allDependencies = new HashSet<>();
		for (CheckableInfo entry : all) {
			DependencyGroup dependencyGroup = dependencyGroupFrom(entry, all);
			if (dependencyGroup != null && !hasJoinedGroups(dependencyGroup, allDependencies)) {
				allDependencies.add(dependencyGroup);
			}
		}
		return allDependencies;
	}

	private static boolean hasJoinedGroups(DependencyGroup dependencyGroup, Set<DependencyGroup> allDependencies) {
		Set<DependencyGroup> joinedGroups = new HashSet<>();
		Set<DependencyGroup> oldGroups = new HashSet<>();

		for (DependencyGroup existingGroup : allDependencies) {
			if (dependencyGroup.canJoin(existingGroup)) {
				dependencyGroup.join(existingGroup);
				joinedGroups.add(dependencyGroup);
			} else {
				oldGroups.add(existingGroup);
			}
		}
		oldGroups.addAll(joinedGroups);
		allDependencies = oldGroups;

		return !joinedGroups.isEmpty();
	}

	private static DependencyGroup dependencyGroupFrom(CheckableInfo entry, Set<CheckableInfo> all) {
		// If result is different from FAIL, this entry has no dependency.
		if (!entry.hasFailed()) {
			return null;
		}
		DependencyGroup dependencyGroup = new DependencyGroup(entry);
		for (CheckableInfo otherInfo : all) {
			if (!otherInfo.name().equals(entry.name())) {

				// Heuristic for test dependency: overlap on the same host VM
				if (entry.hasOverlap(otherInfo) && entry.isSameHostVM(otherInfo)) {
					dependencyGroup.put(otherInfo);
				}
			}
		}
		return dependencyGroup;
	}

	private static void showDependencyModel(Set<DependencyGroup> allDependencies) {
		System.out.println("-------- Dependency Groups --------");
		for (DependencyGroup entry : allDependencies) {
			System.out.println(entry);
		}
	}

	private static void showStatisticsFrom(Set<DependencyGroup> dependencies) {
		// Statistics from allDeps
		int dependencyCounter = 0;
		for (DependencyGroup entry : dependencies) {
			dependencyCounter += entry.size();
		}
		System.out.println("-------- Statistics --------");
		System.out.println(String.format(" %5d %s", dependencies.size(), "Dependency Groups"));
		System.out.println(String.format(" %5d %s ", dependencyCounter, "Dependencies"));
	}

	private static void showRunningInformationFrom(Set<CheckableInfo> entries) {
		System.out.println("-------- Running Information --------");
		int successCounter = 0;
		int failsCounter = 0;
		Set<String> vmCounter = new HashSet<>();
		for (CheckableInfo info : entries) {

			if (info.hasFailed()) {
				failsCounter++;
			} else {
				successCounter++;
			}
			vmCounter.add(info.hostVm());

		}
		System.out.println(String.format(" %5d %s", vmCounter.size(), "VMs used"));
		System.out.println(String.format(" %5d %s", successCounter, "Tests Success"));
		System.out.println(String.format(" %5d %s", failsCounter, "Tests failed"));
	}

}
