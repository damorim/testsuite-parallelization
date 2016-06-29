package br.ufpe.cin.dchecker.model;

import java.util.HashSet;
import java.util.Map.Entry;
import java.util.Set;

public class DependencyGroup {

	private Entry<String, RunningInfo> owner;
	private Set<Entry<String, RunningInfo>> group;

	public DependencyGroup(Entry<String, RunningInfo> from) {
		this.owner = from;
		this.group = new HashSet<Entry<String, RunningInfo>>();
	}

	public int size() {
		return this.group.size();
	}

	public void put(Entry<String, RunningInfo> dependency) {
		this.group.add(dependency);
	}

	public Entry<String, RunningInfo> getOwner() {
		return this.owner;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		String lineSep = System.getProperty("line.separator");
		sb.append(this.owner.getKey()).append(lineSep);
		for (Entry<String, RunningInfo> dep : this.group) {
			sb.append(" => ").append(dep.getKey()).append(lineSep);
		}
		return sb.toString();
	}

}